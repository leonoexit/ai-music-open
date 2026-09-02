"""Application configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Music Open API"
    redis_url: str = "redis://localhost:6379/0"
    queue_name: str = "music-generation"
    output_dir: Path = Path("./data/generated")

    model_path: Path = Path("./models")
    model_version: str = "3B"
    mula_device: str = "cuda"
    codec_device: str = "cuda"
    mula_dtype: str = "bfloat16"
    codec_dtype: str = "float32"
    lazy_load: bool = True

    cors_origins: str = "http://localhost:3000"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
