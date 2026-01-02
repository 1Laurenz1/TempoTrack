from fastapi import Depends

from src.infrastructure.redis.redis_client import get_redis_connection
from src.infrastructure.redis.verification_code_storage import (
    RedisVerificationCodeStorage
)



async def get_redis_verification_code_storage(
        
):
    return RedisVerificationCodeStorage(
        redis = Depends(get_redis_connection)
    )