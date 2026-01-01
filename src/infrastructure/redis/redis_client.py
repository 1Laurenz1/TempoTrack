from redis.asyncio import Redis

from src.infrastructure.config.config_reader import settings


async def get_redis_connection() -> Redis:
    return Redis(
        host=settings.REDSIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True        
    )