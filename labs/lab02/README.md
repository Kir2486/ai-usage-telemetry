# Лабораторная 2. Ответ API -> проверенное событие -> JSONL

## Кейс

API вернул HTTP 200, но в usage пришло отрицательное число токенов. Если просто
загрузить ответ в аналитику, стоимость и агрегаты могут стать неверными. Поэтому
HTTP-успех и валидность данных проверяются отдельно.

Здесь готовый reference-пример для чтения. Он не использует решение lab01.

```text
mock API -> response.raise_for_status() -> JSON -> ProviderResponse
  -> normalize_response() -> UsageEvent -> append_event() -> data/local/usage.jsonl
```

## Файлы и смысл решений

- events.py: модель входа провайдера, модель собственного события, адаптер между ними.
- storage.py: добавление одной записи и повторное чтение с проверкой схемы.
- demo.py: весь путь от запроса до файла; CLI позволяет включить ошибку данных.
- test_events.py: граничные значения, отсутствие usage, повторная запись и повреждённый JSONL.

Числа токенов проверяются строго: строка "10" и bool не принимаются за целое число.
Ноль допустим. observed_at содержит timezone; latency измеряется монотонным
таймером. В mock latency показывает скорость обработки в памяти, не скорость LLM.

Четыре идентификатора отвечают на разные вопросы:

| Поле | Смысл |
|---|---|
| logical_request_id | Какой пользовательской операции принадлежит вызов? |
| attempt_id | Какая это физическая попытка обращения к провайдеру? |
| provider_request_id | Как найти запрос на стороне провайдера? |
| event_id | Как распознать повторную доставку этой же записи? |

## Запуск и ожидаемые результаты

```powershell
.\.venv\Scripts\python.exe -m labs.lab02.demo
Get-Content data/local/usage.jsonl
```

Ожидание: новая строка JSON с input_tokens=1200, output_tokens=200 и UUID. Текст
ответа и prompt в файл не попадают. Каждый новый запуск — новый вызов и новое
событие. Количество строк увеличивается; прежние записи не стираются.

```powershell
.\.venv\Scripts\python.exe -m labs.lab02.demo --scenario invalid
```

Ожидание: REJECTED, сообщение Pydantic о поле usage.input_tokens, exit code 2.
Новая строка в файл не добавляется; существующие записи сохраняются. Ненулевой
exit code в этом сценарии означает, что пример обнаружил заданную ошибку.

## Эксперименты

1. В test_events.py добавить output_tokens=-1. Проверить, что схема отклоняет событие.
2. Передать пустую строку вместо provider_request_id. Где обнаружится ошибка?
3. Удалить поле usage из входа. Сравнить ValidationError с ошибкой HTTP.
4. Посмотреть тест повторной доставки: append_event вызывается дважды с одним event.
   Объяснить, почему две строки имеют один event_id и чем это отличается от двух новых запусков demo.
5. Передать в UsageEvent отрицательную latency или datetime без timezone и добавить тест.

## Границы примера

JSONL sink не дедуплицирует, не защищает от конкурентной записи и не гарантирует
восстановление при аварийном завершении. read_events читает весь файл в память и
останавливается на повреждённой строке. Quarantine для плохих записей, события
ошибок, стоимость, trace_id и outbox пока не реализованы.

English: “We validate usage before storing it. Invalid events must not affect our analytics.”

Источники: [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/),
[serialization](https://docs.pydantic.dev/latest/concepts/serialization/).
