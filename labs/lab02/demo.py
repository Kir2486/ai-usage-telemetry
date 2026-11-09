"""Запуск: python -m labs.lab02.demo [--scenario invalid] [--output PATH]."""

import argparse
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from pydantic import ValidationError

from labs.lab01.mock_provider import make_client
from labs.lab02.events import normalize_response
from labs.lab02.storage import append_event


def run(output: Path, scenario: str) -> int:
    # UUID здесь идентифицирует пользовательскую операцию; новая попытка получает
    # отдельный ID. Не подменяем его ID из ответа провайдера.
    logical_request_id, attempt_id = str(uuid4()), str(uuid4())
    with make_client() as client:
        # Для длительности — монотонный таймер; часы UTC могут корректироваться.
        started = perf_counter()
        response = client.post("/generate", json={"prompt": "Synthetic example"})
        latency_ms = (perf_counter() - started) * 1000
        response.raise_for_status()
        payload = response.json()
        if scenario == "invalid":
            # Намеренная порча входа: покажем, что схема останавливает запись.
            payload["usage"]["input_tokens"] = -10
        try:
            event = normalize_response(
                payload,
                provider_request_id=response.headers["x-request-id"],
                logical_request_id=logical_request_id,
                attempt_id=attempt_id,
                latency_ms=latency_ms,
            )
        except ValidationError as exc:
            # ASCII-сообщение работает и в старых Windows-терминалах с cp1252.
            # Русские пояснения остаются в комментариях и README.
            print("REJECTED: event was not stored; schema validation failed:")
            print(exc)
            return 2
    # Записываем после успешной валидации. Prompts и text в UsageEvent не попадают.
    # Ошибка диска остаётся ошибкой вызова: мы не заявляем доставку, если её не было.
    append_event(output, event)
    print(event.model_dump_json(indent=2))
    print(f"APPENDED: {output.resolve()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["success", "invalid"], default="success")
    parser.add_argument("--output", type=Path, default=Path("data/local/usage.jsonl"))
    args = parser.parse_args()
    return run(args.output, args.scenario)


if __name__ == "__main__":
    raise SystemExit(main())
