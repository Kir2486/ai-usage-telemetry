"""Учебный провайдер: HTTP-объекты настоящие, сеть и LLM не используются.

Начни чтение с make_client(), затем посмотри handle_request().
В реальном клиенте транспорт отправляет байты по сети. Здесь MockTransport
вместо этого вызывает Python-функцию и получает заранее заданный ответ.
"""

import httpx


def handle_request(request: httpx.Request) -> httpx.Response:
    # Метод и путь — часть контракта API. Ошибка адреса должна быть видна,
    # иначе mock мог бы скрыть опечатку в клиенте, отвечая 200 на любой запрос.
    if request.method != "POST" or request.url.path != "/generate":
        return httpx.Response(404, json={"error": "Unknown endpoint"})
    # Request ID находится в заголовке, response ID — в JSON. Это разные сущности.
    # Названия полей синтетические: у реального API контракт нужно читать отдельно.
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
    # Возвращаем клиент, чтобы вызывающий код мог закрыть его через with.
    # timeout задаёт политику реального клиента, но mock не измеряет сетевой timeout.
    return httpx.Client(
        transport=httpx.MockTransport(handle_request),
        base_url="https://mock.invalid",
        timeout=5.0,
    )
