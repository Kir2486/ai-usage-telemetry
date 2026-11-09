# Лабораторная 1. Откуда берутся usage-данные

Первый шаг: посмотреть ответ mock API и извлечь четыре поля. Здесь собственная синтетическая схема, а не точная копия API конкретного провайдера.

## Запуск из корня репозитория

Python 3.12 или новее. Если окружение ещё не подготовлено:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Посмотреть ответ:

```powershell
.\.venv\Scripts\python.exe -m labs.lab01.inspect_response
```

HTTPX MockTransport отвечает прямо в памяти. API-ключ, работающий сервер и платный LLM API не нужны. Это проверка работы с HTTP-объектами, не проверка сети или реальных таймаутов.

## Твоё задание

В starter.py реализуй extract_usage(payload, provider_request_id). Верни плоский словарь с ключами provider_request_id, model, input_tokens, output_tokens. ID запроса передаётся отдельно: его получили из HTTP-заголовка. Поле id в JSON — другой идентификатор.

```powershell
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_exercise.py -q
```

До реализации два теста задания падают с NotImplementedError — это ожидаемое состояние каркаса. Проверки готового mock отдельно:

```powershell
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_mock_provider.py -q
```

Критерий: оба теста задания проходят, пользователь может объяснить происхождение каждого поля. Затем добавим Pydantic, измерение latency и JSONL; отдельными шагами — retries и сбои.

English: “We extract token usage from the provider response.”

Источник: [HTTPX MockTransport](https://www.python-httpx.org/advanced/transports/#mock-transports).
