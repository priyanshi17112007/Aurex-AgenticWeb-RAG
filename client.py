import argparse
import requests


SERVER_URL = "http://127.0.0.1:8000"


def main():
    parser = argparse.ArgumentParser(
        description="Send a query to the FastAPI server."
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="The query text to send to the server.",
    )

    args = parser.parse_args()

    try:
        response = requests.post(
            f"{SERVER_URL}/predict",
            json={"query": args.query},
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()
        print("\nAnswer:\n")
        print(data["output"])

    except requests.exceptions.Timeout:
        print("Error: The server took too long to respond.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the FastAPI server.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
        print(response.text)

    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")

    except KeyError:
        print("Error: The server response does not contain an 'output' field.")


if __name__ == "__main__":
    main()