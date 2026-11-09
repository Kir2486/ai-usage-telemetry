import pytest

from labs.lab01.starter import extract_usage


@pytest.mark.parametrize(
    "model,input_tokens,output_tokens,request_id",
    [("demo-model", 1200, 200, "req_001"), ("other-model", 15, 0, "req_002")],
)
def test_extract_usage(model, input_tokens, output_tokens, request_id):
    payload = {
        "id": "response_id_is_not_request_id",
        "model": model,
        "text": "Not required in a usage event",
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
    }
    assert extract_usage(payload, request_id) == {
        "provider_request_id": request_id,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
