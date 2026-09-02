"""Experimental HeartMuLa engine adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import Settings


class HeartMuLaGenerator:
    """Thin boundary around heartlib so the product is not coupled to its API."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._pipeline: Any | None = None

    def _load_pipeline(self) -> Any:
        if self._pipeline is not None:
            return self._pipeline

        import torch
        from heartlib import HeartMuLaGenPipeline

        dtype_by_name = {
            "float32": torch.float32,
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
        }
        try:
            mula_dtype = dtype_by_name[self.settings.mula_dtype]
            codec_dtype = dtype_by_name[self.settings.codec_dtype]
        except KeyError as error:
            raise ValueError(f"Unsupported model dtype: {error.args[0]}") from error

        self._pipeline = HeartMuLaGenPipeline.from_pretrained(
            str(self.settings.model_path),
            device={
                "mula": torch.device(self.settings.mula_device),
                "codec": torch.device(self.settings.codec_device),
            },
            dtype={"mula": mula_dtype, "codec": codec_dtype},
            version=self.settings.model_version,
            lazy_load=self.settings.lazy_load,
        )
        return self._pipeline

    def generate(
        self,
        *,
        lyrics: str,
        tags: list[str],
        output_path: Path,
        max_audio_length_ms: int,
        topk: int,
        temperature: float,
        cfg_scale: float,
    ) -> Path:
        import torch

        output_path.parent.mkdir(parents=True, exist_ok=True)
        pipeline = self._load_pipeline()
        with torch.inference_mode():
            pipeline(
                {"lyrics": lyrics, "tags": ",".join(tags)},
                save_path=str(output_path),
                max_audio_length_ms=max_audio_length_ms,
                topk=topk,
                temperature=temperature,
                cfg_scale=cfg_scale,
            )
        return output_path
