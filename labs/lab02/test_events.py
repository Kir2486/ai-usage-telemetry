"""Проверяем границы контракта и реальные файлы во временной папке pytest."""

import json
import os
import subprocess
import sys

import pytest
from pydantic import ValidationError

from labs.lab02.demo import run
from labs.lab02.events import normalize_response
from labs.lab02.storage import append_event, read_events


def payload():
    return {"id": "resp_1", "model": "demo", "text": "private synthetic text",
            "usage": {"input_tokens": 10, "output_tokens": 0}}


def normalize(value):
    return normalize_response(value, provider_request_id="req_1",
                              logical_request_id="logical_1", attempt_id="attempt_1",
                              latency_ms=1.5)


@pytest.mark.parametrize("bad_value", [-1, "10", True, None])
def test_invalid_tokens_rejected(bad_value):
    value = payload()
    value["usage"]["input_tokens"] = bad_value
    with pytest.raises(ValidationError):
        normalize(value)


def test_missing_usage_rejected():
    value = payload()
    del value["usage"]
    with pytest.raises(ValidationError):
        normalize(value)


def test_jsonl_roundtrip_and_delivery_identity(tmp_path):
    event = normalize(payload())
    target = tmp_path / "nested" / "usage.jsonl"
    append_event(target, event)
    append_event(target, event)
    loaded = read_events(target)
    # Повторная доставка сохраняет ID, но sink НЕ дедуплицирует. Этот тест
    # фиксирует ограничение, чтобы позже можно было осознанно добавить dedup.
    assert loaded == [event, event]
    assert loaded[0].observed_at.utcoffset().total_seconds() == 0
    saved = json.loads(target.read_text(encoding="utf-8").splitlines()[0])
    assert "text" not in saved and "prompt" not in saved
    assert saved["provider_request_id"] == "req_1"
    assert saved["output_tokens"] == 0


def test_invalid_demo_does_not_create_file(tmp_path):
    target = tmp_path / "rejected.jsonl"
    assert run(target, "invalid") == 2
    assert not target.exists()


def test_success_demo_appends_valid_event(tmp_path):
    target = tmp_path / "usage.jsonl"
    assert run(target, "success") == 0
    assert read_events(target)[0].input_tokens == 1200


def test_corrupt_jsonl_is_not_silently_skipped(tmp_path):
    target = tmp_path / "corrupt.jsonl"
    target.write_text('{"broken":', encoding="utf-8")
    with pytest.raises(ValidationError):
        read_events(target)


def test_invalid_cli_handles_windows_output_encoding(tmp_path):
    # pytest перехватывает stdout в Unicode, поэтому ошибка кодировки может быть
    # видна только при настоящем CLI-запуске. Проверяем отдельный процесс.
    result = subprocess.run(
        [sys.executable, "-m", "labs.lab02.demo", "--scenario", "invalid",
         "--output", str(tmp_path / "invalid.jsonl")],
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "cp1252"},
    )
    assert result.returncode == 2, result.stderr
    assert b"REJECTED" in result.stdout
    assert not (tmp_path / "invalid.jsonl").exists()
