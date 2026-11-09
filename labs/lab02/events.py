"""Контракт события и адаптер ответа провайдера.

Провайдер описывает своё API. Наша платформа задаёт собственный контракт,
чтобы downstream-аналитика не зависела от формы ответа каждого провайдера.
Адаптер — место, где мы явно сопоставляем эти два контракта.
"""

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class ProviderUsage(BaseModel):
    """Ноль токенов допустим; отрицательные числа, строки и bool запрещены."""

    # strict=True защищает от незаметного превращения "1200" или True в число.
    # extra=forbid намеренно требует review при изменении синтетической схемы.
    # Для реального провайдера политику неизвестных полей выбирают отдельно.
    model_config = ConfigDict(strict=True, extra="forbid")
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)


class ProviderResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    id: str = Field(min_length=1)
    model: str = Field(min_length=1)
    text: str
    usage: ProviderUsage


class UsageEvent(BaseModel):
    """Одна успешная попытка вызова, не весь пользовательский workflow.

    event_id должен сохраняться при повторной доставке этой же записи.
    Создать новый event_id при каждом повторе доставки — потерять ключ дедупликации.
    logical_request_id объединяет попытки, attempt_id различает их.
    """

    model_config = ConfigDict(extra="forbid")
    schema_version: int = Field(default=1, strict=True, ge=1)
    event_id: str = Field(min_length=1)
    logical_request_id: str = Field(min_length=1)
    attempt_id: str = Field(min_length=1)
    provider_request_id: str = Field(min_length=1)
    # AwareDatetime требует timezone: без неё дневные агрегаты могут расходиться.
    observed_at: AwareDatetime
    provider: str = "mock"
    model: str = Field(min_length=1)
    input_tokens: int = Field(strict=True, ge=0)
    output_tokens: int = Field(strict=True, ge=0)
    latency_ms: float = Field(ge=0, allow_inf_nan=False)


def normalize_response(
    payload: dict,
    *,
    provider_request_id: str,
    logical_request_id: str,
    attempt_id: str,
    latency_ms: float,
) -> UsageEvent:
    """Готовый reference-пример; упражнение lab01 остаётся отдельным."""
    response = ProviderResponse.model_validate(payload)
    return UsageEvent(
        event_id=str(uuid4()),
        logical_request_id=logical_request_id,
        attempt_id=attempt_id,
        provider_request_id=provider_request_id,
        observed_at=datetime.now(timezone.utc),
        model=response.model,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        latency_ms=latency_ms,
    )
