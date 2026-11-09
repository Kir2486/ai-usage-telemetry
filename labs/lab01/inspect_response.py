"""Run from repository root: python -m labs.lab01.inspect_response."""

import json

from labs.lab01.mock_provider import make_client


def main() -> None:
    # with освобождает ресурсы клиента даже при исключении внутри блока.
    with make_client() as client:
        response = client.post("/generate", json={"prompt": "Summarize a document"})
        # Сначала HTTP-статус, затем разбор бизнес-данных. JSON с сообщением об
        # ошибке не должен случайно обрабатываться как успешный ответ модели.
        response.raise_for_status()
        print("HTTP status:", response.status_code)
        print("Provider request ID:", response.headers["x-request-id"])
        # response.json() превращает тело JSON в Python-объект (здесь dict).
        # Это ещё не валидация схемы: обязательных полей может не оказаться.
        print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
