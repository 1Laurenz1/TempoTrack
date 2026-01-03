from fastapi import Depends

from src.infrastructure.redis.redis_client import get_redis_connection
from src.infrastructure.redis.verification_code_storage import (
    RedisVerificationCodeStorage
)
from src.infrastructure.redis.telegram_indetify_storage import (
    RedisTelegramIndetifyStorage
)



async def get_redis_verification_code_storage():
    redis = await get_redis_connection()
    
    return RedisVerificationCodeStorage(redis=redis)


async def get_redis_telegram_indetify_storage():
    redis = await get_redis_connection()
    
    return RedisTelegramIndetifyStorage(
        redis=redis
    )