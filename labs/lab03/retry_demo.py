"""Симуляция политики retries; не реализация production LLM gateway.

Запуск: python -m labs.lab03.retry_demo --scenario rate-limit
Сначала изучи call_with_retry(), затем сценарии и тесты.
"""

import argparse
from collections.abc import Callable
from dataclasses import dataclass
from time import sleep
from uuid import uuid4

import httpx

from labs.lab01.mock_provider import handle_request


@dataclass(frozen=True)
class Attempt:
    """Неуспешный вызов тоже имеет attempt_id, даже если usage неизвестен."""

    logical_request_id: str
    attempt_id: str
    number: int
    outcome: str


class ScenarioProvider:
    """Состояние mock принадлежит одному сценарию, не глобальному процессу."""

    def __init__(self, outcomes: list[int | str]):
        if not outcomes:
            raise ValueError("Нужен хотя бы один outcome")
        self.outcomes = outcomes
        self.calls = 0

    def __call__(self, request: httpx.Request) -> httpx.Response:
        outcome = self.outcomes[min(self.calls, len(self.outcomes) - 1)]
        self.calls += 1
        if outcome == "timeout":
            # Исключение поднимается явно. Медленный mock сам по себе не проверяет
            # работу сетевых таймеров HTTPX. Это симуляция уже возникшего ReadTimeout.
            raise httpx.ReadTimeout("Synthetic read timeout", request=request)
        if outcome == 200:
            return handle_request(request)
        return httpx.Response(int(outcome), json={"error": "Synthetic failure"})


def call_with_retry(
    client: httpx.Client,
    attempts: list[Attempt],
    *,
    max_attempts: int = 3,
    wait: Callable[[float], None] = sleep,
) -> dict:
    """Повторяем только 429 и 503; всего max_attempts вызовов, не повторов.

    Эта политика допустима для синтетического API. Для реального генеративного
    API повторный POST может создать ещё одну генерацию и дополнительный расход.
    Нужны гарантии провайдера/idempotency, а не только проверка кода статуса.
    Retry-After и jitter здесь намеренно оставлены отдельным упражнением.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts должен быть >= 1")
    logical_id = str(uuid4())
    for number in range(1, max_attempts + 1):
        attempt_id = str(uuid4())
        try:
            response = client.post("/generate", json={"prompt": "Synthetic example"})
        except httpx.ReadTimeout:
            # Не знаем, выполнил ли провайдер запрос. Не записываем нулевой расход
            # и не повторяем автоматически: потребуется reconciliation.
            attempts.append(Attempt(logical_id, attempt_id, number, "unknown_timeout"))
            raise
        attempts.append(Attempt(logical_id, attempt_id, number, str(response.status_code)))
        if response.status_code in {429, 503} and number < max_attempts:
            # Backoff 0.1, 0.2, ...; wait внедряется, чтобы тесты не спали.
            # Ограничение числа попыток защищает от бесконечного цикла и нагрузки.
            wait(0.1 * 2 ** (number - 1))
            continue
        response.raise_for_status()
        return response.json()
    raise AssertionError("Цикл обязан вернуть ответ или поднять исключение")


SCENARIOS = {
    "success": [200],
    "rate-limit": [429, 200],
    "unavailable": [503, 503, 200],
    "exhausted": [503],
    "unauthorized": [401],
    "timeout": ["timeout", 200],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, default="rate-limit")
    args = parser.parse_args()
    provider = ScenarioProvider(SCENARIOS[args.scenario])
    attempts: list[Attempt] = []
    try:
        with httpx.Client(transport=httpx.MockTransport(provider),
                          base_url="https://mock.invalid", timeout=5) as client:
            result = call_with_retry(client, attempts)
            print("SUCCESS:", result["usage"])
        return 0
    except httpx.HTTPError as exc:
        print(f"STOPPED: {type(exc).__name__}: {exc}")
        return 2
    finally:
        for attempt in attempts:
            print(attempt)


if __name__ == "__main__":
    raise SystemExit(main())
