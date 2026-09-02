"""Redis queue connections."""

from redis import Redis
from rq import Queue

from .config import get_settings


def get_redis() -> Redis:
    settings = get_settings()
    return Redis.from_url(settings.redis_url)


def get_generation_queue() -> Queue:
    settings = get_settings()
    return Queue(settings.queue_name, connection=get_redis())
