import json

from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from core.settings import settings
from schemas import v1 as schemas_v1

redis = Redis(host="redis", port=settings.REDIS_PORT)


def redis_cache(key_prefix: str):
    def decorator(func):
        async def wrapper(input_data: schemas_v1.Review):
            key = f"{key_prefix}:{json.dumps(jsonable_encoder(input_data))}"
            cached_result = await redis.get(key)
            if cached_result:
                return json.loads(cached_result)
            result = await func(input_data)
            await redis.set(key, json.dumps(result, default=str), ex=3600)
            return result

        return wrapper

    return decorator
