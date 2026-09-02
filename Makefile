.PHONY: install install-gpu test lint api worker web infra

install:
	python -m pip install -e ".[dev]"

install-gpu:
	python -m pip install -e ".[dev,gpu]"

test:
	pytest

lint:
	ruff check .

api:
	uvicorn ai_music_open.api:app --reload

worker:
	rq worker --url "$${REDIS_URL:-redis://localhost:6379/0}" "$${QUEUE_NAME:-music-generation}"

web:
	cd apps/web && npm run dev

infra:
	docker compose up redis api web
