"""Run from repository root: python -m labs.lab01.inspect_response."""

import json

from labs.lab01.mock_provider import make_client


def main() -> None:
    with make_client() as client:
        response = client.post("/generate", json={"prompt": "Summarize a document"})
        response.raise_for_status()
        print("HTTP status:", response.status_code)
        print("Provider request ID:", response.headers["x-request-id"])
        print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
