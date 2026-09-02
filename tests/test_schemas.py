import pytest
from pydantic import ValidationError

from ai_music_open.schemas import GenerationCreate


def test_generation_request_normalizes_tags() -> None:
    request = GenerationCreate(
        lyrics="[Verse]\nHello",
        tags=[" Pop ", "happy", "pop"],
    )

    assert request.tags == ["pop", "happy"]


def test_generation_request_rejects_blank_lyrics() -> None:
    with pytest.raises(ValidationError):
        GenerationCreate(lyrics="   ", tags=["pop"])
