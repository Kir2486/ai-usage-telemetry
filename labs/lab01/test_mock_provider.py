from labs.lab01.mock_provider import make_client


def test_successful_provider_response():
    with make_client() as client:
        response = client.post("/generate", json={"prompt": "Example"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req_demo_001"
    assert response.json()["usage"] == {"input_tokens": 1200, "output_tokens": 200}


def test_unknown_endpoint():
    with make_client() as client:
        response = client.post("/unknown")
    assert response.status_code == 404
