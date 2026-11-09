# Практическая лаборатория

Это материалы для самостоятельного изучения: готовые демонстрации с комментариями,
проверки и отдельные задания. Читать весь каталог за один раз не нужно.

| Порядок | Тема | Что посмотреть | Что сделать самостоятельно |
|---|---|---|---|
| 1 | [Ответ API](lab01/README.md) | mock_provider.py -> inspect_response.py | Реализовать starter.extract_usage |
| 2 | [Контракт и JSONL](lab02/README.md) | events.py -> storage.py -> demo.py -> test_events.py | Эксперименты с типами, полями и дубликатами |
| 3 | [Retries и timeout](lab03/README.md) | retry_demo.py -> test_retry.py | Добавить новый сценарий и проверить границы политики |

## Быстрый старт

Из корня проекта после подготовки .venv:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m labs.lab01.inspect_response
.\.venv\Scripts\python.exe -m labs.lab02.demo
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario rate-limit
```

Проверить все готовые демонстрации:

```powershell
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_mock_provider.py labs/lab02 labs/lab03 -q
```

Проверить только своё упражнение:

```powershell
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_exercise.py -q
```

Общий pytest включает незавершённое упражнение и потому пока показывает два
ожидаемых падения. Они не скрыты через skip: после твоей реализации эти же тесты
должны стать зелёными. Готовые примеры не вызывают starter.py.

## Как изучать код

1. Прочитать README нужной лабораторной и предсказать результат команды.
2. Запустить пример и сравнить вывод с ожиданием.
3. Открыть тест: посмотреть вход, действие и assert.
4. Поменять один параметр или добавить сценарий; снова запустить проверку.
5. Объяснить, что произошло, почему и какое ограничение осталось.

Сохраняй собственные наблюдения в заметках к упражнению; после review обновим
PROGRESS.md. Успех reference-тестов подтверждает демонстрацию, не освоение темы.

Дальше по плану: учёт стоимости и cached tokens, async/concurrency, надёжная
доставка, OpenTelemetry. Они ещё не реализованы в этих трёх лабораторных.
