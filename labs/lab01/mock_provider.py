"""Synthetic API; all requests handled in memory, without network access."""

import httpx


def handle_request(request: httpx.Request) -> httpx.Response:
    if request.method != "POST" or request.url.path != "/generate":
        return httpx.Response(404, json={"error": "Unknown endpoint"})
    return httpx.Response(
        200,
        headers={"x-request-id": "req_demo_001"},
        json={
            "id": "response_demo_001",
            "model": "demo-model",
            "text": "A synthetic answer.",
            "usage": {"input_tokens": 1200, "output_tokens": 200},
        },
    )


def make_client() -> httpx.Client:
    return httpx.Client(
        transport=httpx.MockTransport(handle_request),
        base_url="https://mock.invalid",
        timeout=5.0,
    )
