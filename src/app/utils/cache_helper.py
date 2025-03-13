import redis
import json
from src.app.utils.constants import (
    REDIS_HOST, REDIS_PORT, CACHE_EXPIRY
)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cache_events(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None


def set_cached_events(key: str, data):
    redis_client.setex(name=key, time=CACHE_EXPIRY, value=json.dumps(data))



