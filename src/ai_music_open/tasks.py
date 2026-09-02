"""Asynchronous generation tasks."""

from __future__ import annotations

from typing import Any

from rq import get_current_job

from .config import get_settings
from .generator import HeartMuLaGenerator

_generator: HeartMuLaGenerator | None = None


def get_generator() -> HeartMuLaGenerator:
    global _generator
    if _generator is None:
        _generator = HeartMuLaGenerator(get_settings())
    return _generator


def generate_music(generation_id: str, payload: dict[str, Any]) -> dict[str, str]:
    settings = get_settings()
    job = get_current_job()
    if job is not None:
        job.meta["stage"] = "generating"
        job.save_meta()

    output_path = settings.output_dir / f"{generation_id}.mp3"
    generator = get_generator()
    generator.generate(output_path=output_path, **payload)

    if job is not None:
        job.meta["stage"] = "complete"
        job.save_meta()
    return {"output_path": str(output_path)}
