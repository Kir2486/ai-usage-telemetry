# Разработка и продолжение на другом ПК

## Что нужно установить отдельно на каждом компьютере

- Git.
- Python 3.12 или новее (команды ниже используют python; в Windows можно заменить на py -3.12).
- GitHub CLI (gh) для создания PR и управления репозиторием. Для обычных clone/pull/push достаточно Git с настроенной авторизацией.

Вход в gh выполняется пользователем на каждом ПК отдельно:

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git --hostname github.com
```

Не копировать credentials или .venv между компьютерами.

## Первое открытие проекта

```powershell
git clone https://github.com/Kir2486/ai-usage-telemetry.git
cd ai-usage-telemetry
git fetch origin
git switch codex/lab-01-llm-usage
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Ветка приведена для первой лабораторной. Для следующих этапов сверять актуальную ветку с PROGRESS.md и git branch -a. В Linux/macOS путь Python окружения — .venv/bin/python.

requirements-dev.txt задаёт прямые зависимости, requirements-lock.txt фиксирует проверенные версии вместе с транзитивными зависимостями. Фиксация получена на Windows с Python 3.12; другие ОС отдельно не проверены.

## Команды лабораторных

```powershell
.\.venv\Scripts\python.exe -m labs.lab01.inspect_response
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_mock_provider.py -q
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_exercise.py -q
.\.venv\Scripts\python.exe -m labs.lab02.demo
.\.venv\Scripts\python.exe -m labs.lab03.retry_demo --scenario rate-limit
.\.venv\Scripts\python.exe -m pytest labs/lab01/test_mock_provider.py labs/lab02 labs/lab03 -q
```

Проверки mock должны проходить. Два теста упражнения ожидаемо падают с NotImplementedError, пока пользователь не реализовал extract_usage. Это учебная заготовка, не готовая production-интеграция. MockTransport работает в памяти и не проверяет реальные сетевые сбои.

## Два компьютера

Перед началом посмотреть git status --short --branch. При чистой рабочей папке выполнить git pull --ff-only в нужной ветке. Если есть изменения, сначала разобраться с ними; не применять reset/clean и не затирать работу.

После занятия: запустить подходящие проверки, обновить PROGRESS.md, проверить git diff, сделать небольшой коммит и git push. На другом ПК перейти в ту же ветку и обновить её. Один GitHub-аккаунт не синхронизирует незакоммиченные файлы автоматически.

## Передача другой LLM

Передать ей этот запрос:

> Прочитай AGENTS.md, docs/CONTEXT.md, docs/PROGRESS.md и docs/DEVELOPMENT.md. Проверь текущую ветку и рабочую папку. Продолжай с следующего шага в прогрессе, короткими уроками на русском. Не реализуй основную учебную логику без моего запроса. Сначала кратко сообщи, на каком этапе проект.

Файлы — общий источник контекста для любых моделей. Автоматическое чтение AGENTS.md зависит от клиента; если оно не поддерживается, попросить прочитать файл явно.
