from typing import Optional
from redis.asyncio import Redis

from src.application.ports.verification_code_storage import VerificationCodeStorage


class RedisVerificationCodeStorage(VerificationCodeStorage):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_verification_code(
        self,
        user_id: int,
        code: str,
        ttl_seconds: int = 300,
    ) -> str:
        await self.redis.set(
            f"verify:{user_id}",
            code,
            ex=ttl_seconds,
        )


    async def get_verify_code_by_user_id(
        self,
        user_id: int    
    ) -> Optional[str]:
        code = await self.redis.get(
            name=f"verify:{user_id}"
        )
        
        return code if code else None


    async def delete_code(
        self,
        user_id: int
    ) -> None:
        return await self.redis.delete(
            f"verify:{user_id}"
        )