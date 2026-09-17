# 🤖 Aurex AgenticWeb RAG

<p align="center">
  <img src="https://img.shields.io/badge/Agentic-AI-7C3AED?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Web-RAG-2563EB?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FastAPI-Production-009688?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Groq-LLM-00A67E?style=for-the-badge"/>
</p>

<p align="center">
  <strong>Real-Time Agentic Web Retrieval-Augmented Generation Platform</strong>
</p>

<p align="center">
  Built with <b>CrewAI</b>, <b>Groq LLM</b>, <b>Serper API</b>, <b>LiteLLM</b>, and <b>FastAPI</b>. This platform performs live internet research and generates grounded AI responses through a production-ready REST API, terminal CLI, and a premium glassmorphic web interface.
</p>

---

## 🛠 Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,html,css,js,git,vscode" />
</p>

| **Category**    | **Technology**                    |
| --------------- | --------------------------------- |
| Language        | Python 3.10+                      |
| Agent Framework | CrewAI                            |
| LLM Gateway     | LiteLLM                           |
| LLM Engine      | Groq GPT-OSS 120B                 |
| Web Retrieval   | Serper API                        |
| Backend         | FastAPI · Uvicorn · LitServe      |
| Validation      | Pydantic                          |
| Frontend        | HTML5 · CSS3 · Vanilla JavaScript |

---

## ✨ Key Features

* 🌐 **Real-Time Web Retrieval** using Serper API
* 🤖 **Single Agentic Writer Workflow** powered by CrewAI
* ⚡ **Ultra-FFast Inference** with Groq + LiteLLM
* 🔍 **Search-Augmented Generation (Web RAG)**
* 🚀 **Production-Ready FastAPI REST API**
* 💻 **Dual Interface** — Terminal CLI & Luxury Glassmorphic Web UI
* 💎 **Responsive Gold Glassmorphism Design**
* 🛡️ **Prompt-Safe Architecture** with controlled tool execution

---

## 🏗 Architecture

```text
                    User Query
                         │
        ┌────────────────┴────────────────┐
        │                                 │
  Terminal CLI                     Web Frontend
   (client.py)                     (index.html)
        │                                 │
        └────────────────┬────────────────┘
                         │
                    FastAPI Server
                         │
                 Python search_web()
                         │
                  SerperDevTool API
                         │
                Retrieved Web Evidence
                         │
                CrewAI Writer Agent
                         │
                 LiteLLM → Groq LLM
                         │
                 Grounded AI Response
```

---

## ⚙ Request Processing Pipeline

| **Component**         | **Responsibility**                                   |
| --------------------- | ---------------------------------------------------- |
| FastAPI               | Receives user requests and exposes REST endpoints    |
| Python `search_web()` | Executes real-time web retrieval                     |
| SerperDevTool         | Fetches relevant search results from the web         |
| CrewAI                | Orchestrates the Writer Agent workflow               |
| Writer Agent          | Synthesizes retrieved evidence into the final answer |
| LiteLLM               | Connects CrewAI with the Groq model                  |
| Groq LLM              | Generates the final natural language response        |

---

## 🚀 Core Capabilities

* Real-time Internet Search
* Agentic AI Orchestration
* Grounded Question Answering
* REST API Deployment
* Prompt Augmentation
* Low-Latency LLM Inference
* JSON-based Prediction Endpoint
* Responsive Glassmorphic Interface

---

## 📂 Project Structure

```text
Aurex-AgenticWeb-RAG/
│
├── server.py          # FastAPI + RAG Pipeline
├── client.py          # Terminal CLI
├── index.html         # Glassmorphic Frontend
├── .gitignore
└── README.md
```

---

## ⚡ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/priyanshi17112007/Aurex-AgenticWeb-RAG.git
cd Aurex-AgenticWeb-RAG
```

### 2. Create & Activate Virtual Environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
crewai
crewai-tools
fastapi
uvicorn
python-dotenv
litellm
requests
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## ▶ Run the Application

### Start Backend

```bash
python server.py
```

or

```bash
uvicorn server:app --reload
```

**API Endpoint**

```text
http://127.0.0.1:8000/predict
```

**Swagger Documentation**

```text
http://127.0.0.1:8000/docs
```

### Run Terminal Client

```bash
python client.py
```

### Launch Web Interface

```bash
python -m http.server 5500
```

Open in your browser:

```text
http://127.0.0.1:5500/index.html
```

---

## 🎯 Why This Project Stands Out

| **Traditional RAG**         | **Aurex AgenticWeb RAG**       |
| --------------------------- | ------------------------------ |
| Static knowledge base       | Live web intelligence          |
| Vector database required    | No vector database             |
| Offline document retrieval  | Real-time internet retrieval   |
| Generic LLM pipeline        | Agentic CrewAI workflow        |
| Limited knowledge freshness | Current information generation |

---

## 📈 Future Enhancements

* Hybrid Web + ChromaDB RAG
* Source citation rendering
* Conversation memory
* Streaming token responses
* Authentication & User Sessions
* Confidence scoring
* Production logging & monitoring

---

## 👩‍💻 Author

**Priyanshi Sharma**

*Agentic AI Enthusiast • Python Developer • AI Automation Builder*

<p align="left">
  <a href="https://github.com/priyanshi17112007">
    <img src="https://img.shields.io/badge/GitHub-priyanshi17112007-181717?style=for-the-badge&logo=github"/>
  </a>
</p>

---

