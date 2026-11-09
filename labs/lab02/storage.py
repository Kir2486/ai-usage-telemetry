"""JSONL: одна JSON-запись на строку, удобно читать и исследовать.

Это локальный учебный sink для одного процесса. Здесь нет fsync, транзакций,
защиты от конкурентной записи, автоматического восстановления оборванной строки
или дедупликации. Успешный close не означает гарантированную сохранность при сбое ОС.
"""

from pathlib import Path

from labs.lab02.events import UsageEvent


def append_event(path: Path, event: UsageEvent) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # mode=a добавляет запись, а не стирает предыдущие. model_dump_json()
    # корректно сериализует datetime; перевод строки завершает JSONL-запись.
    with path.open("a", encoding="utf-8") as stream:
        stream.write(event.model_dump_json() + "\n")


def read_events(path: Path) -> list[UsageEvent]:
    # Читаем обратно с проверкой схемы, чтобы повреждённые данные не проходили тихо.
    # Для больших файлов нужен потоковый iterator, а не список в памяти.
    with path.open(encoding="utf-8") as stream:
        return [UsageEvent.model_validate_json(line) for line in stream]
