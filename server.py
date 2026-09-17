import os
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv

# Load environment variables before initializing CrewAI tools.
load_dotenv()

# Workaround for some CrewAI versions that send the unsupported
# cache_breakpoint field to Groq.
try:
    import crewai.llms.cache as crewai_cache

    def disable_cache_breakpoint(message, *args, **kwargs):
        return message

    crewai_cache.mark_cache_breakpoint = disable_cache_breakpoint

except ImportError:
    # Some CrewAI versions do not contain this module.
    # In that case, no patch is required.
    pass


from crewai import Agent, Crew, LLM, Task
from crewai_tools import SerperDevTool
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add GROQ_API_KEY to your .env file."
    )

if not SERPER_API_KEY:
    raise RuntimeError(
        "SERPER_API_KEY is missing. Add SERPER_API_KEY to your .env file."
    )

# SerperDevTool reads this environment variable internally.
os.environ["SERPER_API_KEY"] = SERPER_API_KEY


# -------------------------------------------------------------------
# Request and response models
# -------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The question to research and answer.",
    )


class QueryResponse(BaseModel):
    output: str


class HealthResponse(BaseModel):
    status: str
    service_ready: bool


# -------------------------------------------------------------------
# Agentic RAG service
# -------------------------------------------------------------------

class AgenticRAGService:
    def __init__(self):
        # Current Groq model.
        #
        # Do not use:
        # groq/llama-3.3-70b-versatile
        #
        # The provider prefix is required by CrewAI/LiteLLM.
        self.llm = LLM(
            model="groq/openai/gpt-oss-120b",
            api_key=GROQ_API_KEY,
            temperature=0.2,
            reasoning_effort="low",
            max_tokens=1000,
        )

        # The search tool is executed directly by Python.
        # It is intentionally NOT passed to the LLM agent.
        self.search_tool = SerperDevTool()

        self.writer = Agent(
            role="Factual Answer Writer",
            goal=(
                "Write a concise, accurate answer using only the supplied "
                "web research."
            ),
            backstory=(
                "You are a professional technical writer. You summarize "
                "research clearly and never invent information."
            ),
            llm=self.llm,
            tools=[],
            allow_delegation=False,
            max_iter=2,
            verbose=True,
        )

    def search_web(self, query: str) -> str:
        """
        Execute Serper directly instead of allowing the LLM to call tools.

        This prevents errors such as:
        attempted to call tool 'open_file'
        """

        try:
            # SerperDevTool normally expects the argument search_query.
            result = self.search_tool.run(search_query=query)
        except TypeError:
            # Compatibility fallback for versions expecting a positional value.
            result = self.search_tool.run(query)

        if result is None:
            return "No search results were returned."

        result_text = str(result)

        # Prevent very large search context from consuming the Groq TPM limit.
        maximum_search_characters = 8000

        if len(result_text) > maximum_search_characters:
            result_text = result_text[:maximum_search_characters]
            result_text += "\n\n[Search results truncated]"

        return result_text

    def generate_answer(self, query: str, research: str) -> str:
        """
        Use a tool-free CrewAI writer to summarize the search results.
        """

        writing_task = Task(
            description=(
                "Answer the user's question using only the research below.\n\n"
                "Rules:\n"
                "1. Do not use tools.\n"
                "2. Do not open URLs or files.\n"
                "3. Do not invent facts or sources.\n"
                "4. If the research is insufficient, say so clearly.\n"
                "5. Keep the answer UPTO 500 words.\n"
                "6. Include important dates when relevant.\n\n"
                f"User question:\n{query}\n\n"
                f"Web research:\n{research}"
            ),
            expected_output=(
                "A concise, factual answer based only on the supplied research."
            ),
            agent=self.writer,
        )

        writer_crew = Crew(
            agents=[self.writer],
            tasks=[writing_task],
            verbose=True,
        )

        result = writer_crew.kickoff()

        # CrewAI usually returns a CrewOutput object with a raw property.
        if hasattr(result, "raw"):
            return str(result.raw).strip()

        return str(result).strip()

    def ask(self, query: str) -> str:
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        print(f"Searching the web for: {query}")

        research = self.search_web(query)

        if not research.strip():
            raise RuntimeError("The search tool returned no research results.")

        print("Generating final answer...")

        return self.generate_answer(query, research)


# -------------------------------------------------------------------
# FastAPI application
# -------------------------------------------------------------------

service: AgenticRAGService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global service

    try:
        service = AgenticRAGService()
        print("Agentic RAG service started successfully.")
        yield

    finally:
        service = None
        print("Agentic RAG service stopped.")


app = FastAPI(
    title="Agentic RAG API",
    description="Web search and factual answer generation using Groq and CrewAI.",
    version="1.0.0",
    lifespan=lifespan,
)


# Allow requests from your frontend.
# For production, replace "*" with your frontend URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# API routes
# -------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "message": "Agentic RAG API is running.",
        "docs": "/docs",
        "predict_endpoint": "POST /predict",
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service_ready=service is not None,
    )


@app.post("/predict", response_model=QueryResponse)
async def predict(request: QueryRequest):
    if service is None:
        raise HTTPException(
            status_code=503,
            detail="The Agentic RAG service is not ready.",
        )

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    try:
        # CrewAI and Serper calls are synchronous, so run them in a thread.
        answer = await run_in_threadpool(service.ask, query)

        return QueryResponse(output=answer)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        error_text = str(error).lower()

        # Return HTTP 429 when Groq's token-per-minute limit is reached.
        if (
            "rate limit" in error_text
            or "ratelimit" in error_text
            or "rate_limit_exceeded" in error_text
            or "tokens per minute" in error_text
            or "tpm" in error_text
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "Groq rate limit reached. "
                    "Please wait approximately 30 to 60 seconds "
                    "before trying again."
                ),
                headers={"Retry-After": "35"},
            ) from error

        print(f"Prediction error: {error}")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate an answer: {error}",
        ) from error


# -------------------------------------------------------------------
# Local development entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )