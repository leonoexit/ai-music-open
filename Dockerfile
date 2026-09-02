FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
RUN apt-get update \
    && apt-get install --no-install-recommends -y ffmpeg git libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

FROM base AS api
EXPOSE 8000
CMD ["uvicorn", "ai_music_open.api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS worker
RUN pip install --no-cache-dir ".[gpu]"
CMD ["rq", "worker", "--url", "redis://redis:6379/0", "music-generation"]
