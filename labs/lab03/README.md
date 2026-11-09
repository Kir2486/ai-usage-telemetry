# Лабораторная 3. Retries, лимиты и неизвестный результат

## Кейс

Провайдер временно отвечает 429, затем 200. Клиент может подождать и повторить
запрос. Но бесконечные повторы увеличивают нагрузку и могут увеличить расходы.
Мы явно задаём лимит попыток и сохраняем историю каждого обращения.

Готовая демонстрация работает в памяти. Она не подключена к JSONL из lab02:
пока отдельно изучаем политику повторов, затем спроектируем общий поток attempts.

## Команды из корня репозитория

```powershell
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario success
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario rate-limit
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario unavailable
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario exhausted
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario unauthorized
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario timeout
```

| Сценарий | Ответы mock | Что ожидаем |
|---|---|---|
| success | 200 | Одна попытка, SUCCESS, exit 0 |
| rate-limit | 429, 200 | Две попытки, ожидание 0.1 сек., exit 0 |
| unavailable | 503, 503, 200 | Три попытки, ожидания 0.1 и 0.2 сек., exit 0 |
| exhausted | Всегда 503 | Три попытки, STOPPED, exit 2 |
| unauthorized | 401 | Одна попытка, STOPPED, exit 2 |
| timeout | ReadTimeout, затем возможный 200 | Одна попытка, unknown_timeout, STOPPED, exit 2 |

Сравни logical_request_id и attempt_id в выводе: первая величина общая для
операции, вторая меняется при каждой попытке. Номер попытки начинается с 1.
max_attempts=3 означает максимум три обращения, то есть максимум два повтора.

## В каком порядке читать код

1. Attempt — какие сведения остаются даже при ошибке.
2. call_with_retry — цикл, ограничения, обработка ReadTimeout и HTTP-статусов.
3. ScenarioProvider — как искусственно создаётся сбой.
4. test_retry.py — почему ожидание внедрено через функцию wait.

В тесте передаём wait=waits.append: вместо ожидания сохраняется его длительность.
Так проверяется расписание backoff без медленных и нестабильных тестов.

## Почему не повторяем timeout автоматически

ReadTimeout означает, что клиент не дождался данных. Провайдер мог уже выполнить
генерацию. Повторный POST может создать ещё один платный вызов. В примере сохраняем
unknown_timeout и останавливаемся. Это выбранная консервативная политика; реальное
решение зависит от API, idempotency и допустимого риска повторного начисления.

Нельзя объявлять такую попытку бесплатной или записывать usage=0 только потому,
что ответ не пришёл. Для учёта потребуется дальнейшая сверка с провайдером.

## Твои эксперименты

1. Добавить сценарий [429, 401, 200]. До какой попытки дойдёт клиент?
2. Вызвать call_with_retry с max_attempts=1 и ответом 503. Сколько вызовов wait?
3. Добавить тест 500. Текущая политика его не повторяет: стоит ли менять её для выбранного API?
4. Спроектировать поддержку Retry-After: что делать с HTTP-date, неверным значением и слишком большой задержкой?
5. Объяснить, как jitter помогает клиентам не повторять запросы одновременно.

Retry-After, jitter, общий deadline, async, circuit breaker и учёт полной истории
в хранилище — следующие расширения. Этот код не является универсальной retry-политикой.

English: “We limit retries and track each attempt. A timeout does not prove that the provider did not process the request.”

Источники: [HTTPX exceptions](https://www.python-httpx.org/exceptions/),
[MockTransport](https://www.python-httpx.org/advanced/transports/#mock-transports).
