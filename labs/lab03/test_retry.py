"""Проверяем поведение, а не ждём реальный backoff в тестах."""

import httpx
import pytest

from labs.lab03.retry_demo import ScenarioProvider, call_with_retry


@pytest.mark.parametrize("codes,expected_waits", [([200], []), ([429, 200], [0.1]),
                                               ([503, 503, 200], [0.1, 0.2])])
def test_success_after_bounded_retries(codes, expected_waits):
    provider = ScenarioProvider(codes)
    attempts, waits = [], []
    with httpx.Client(transport=httpx.MockTransport(provider), base_url="https://mock.invalid") as client:
        result = call_with_retry(client, attempts, wait=waits.append)
    assert result["usage"]["input_tokens"] == 1200
    assert waits == expected_waits
    assert provider.calls == len(codes)
    assert len({a.logical_request_id for a in attempts}) == 1
    assert len({a.attempt_id for a in attempts}) == len(codes)


@pytest.mark.parametrize("code,expected_calls", [(401, 1), (400, 1), (503, 3), (429, 3)])
def test_permanent_failure_or_exhausted_budget(code, expected_calls):
    provider = ScenarioProvider([code])
    attempts, waits = [], []
    with httpx.Client(transport=httpx.MockTransport(provider), base_url="https://mock.invalid") as client:
        with pytest.raises(httpx.HTTPStatusError):
            call_with_retry(client, attempts, wait=waits.append)
    assert provider.calls == expected_calls
    assert len(waits) == expected_calls - 1  # Не спим после последней попытки.


def test_timeout_stops_without_guessing_usage():
    provider = ScenarioProvider(["timeout", 200])
    attempts, waits = [], []
    with httpx.Client(transport=httpx.MockTransport(provider), base_url="https://mock.invalid") as client:
        with pytest.raises(httpx.ReadTimeout):
            call_with_retry(client, attempts, wait=waits.append)
    assert provider.calls == 1
    assert attempts[0].outcome == "unknown_timeout"
    assert waits == []


def test_invalid_budget_never_calls_provider():
    provider = ScenarioProvider([200])
    with httpx.Client(transport=httpx.MockTransport(provider), base_url="https://mock.invalid") as client:
        with pytest.raises(ValueError):
            call_with_retry(client, [], max_attempts=0)
    assert provider.calls == 0
