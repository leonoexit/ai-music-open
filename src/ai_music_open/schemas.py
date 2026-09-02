"""API request and response schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class GenerationCreate(BaseModel):
    lyrics: str = Field(min_length=1, max_length=20_000)
    tags: list[str] = Field(min_length=1, max_length=30)
    max_audio_length_ms: int = Field(default=120_000, ge=10_000, le=240_000)
    topk: int = Field(default=50, ge=1, le=500)
    temperature: float = Field(default=1.0, gt=0, le=2.0)
    cfg_scale: float = Field(default=1.5, ge=1.0, le=5.0)

    @field_validator("lyrics")
    @classmethod
    def normalize_lyrics(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("lyrics cannot be blank")
        return value

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, values: list[str]) -> list[str]:
        normalized = [value.strip().lower() for value in values if value.strip()]
        if not normalized:
            raise ValueError("at least one non-empty tag is required")
        return list(dict.fromkeys(normalized))


GenerationState = Literal[
    "queued",
    "started",
    "finished",
    "failed",
    "deferred",
    "scheduled",
    "stopped",
    "canceled",
]


class GenerationStatus(BaseModel):
    id: str
    status: GenerationState
    output_url: str | None = None
    error: str | None = None


class HealthStatus(BaseModel):
    status: Literal["ok", "degraded"]
    redis: Literal["ok", "unavailable"]
