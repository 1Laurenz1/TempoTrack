from typing import Optional
from redis.asyncio import Redis

from src.common.utils.get_verification_code import generate_verification_code


class RedisSerivce:
    def __init__(
        self,
        redis: Redis
    ):
        self.redis = redis
        
        
    async def set_verification_code(
        self,
        user_id: int,
        ttl_seconds: int = 300,
    ):
        code = generate_verification_code()
        
        await self.redis.set(
            name=f"verify:{user_id}",
            value=code,
            ex=ttl_seconds
        )
        
        return code
    
    
    async def get_verify_code_by_user_id(
        self,
        user_id: int
    ) -> Optional[str]:
        code = await self.redis.get(
            name=f"verify:{user_id}"
        )
        
        if not code:
            return None
        return code
    
    
    async def delete_code(
        self,
        user_id: int
    ) -> bool:
        return await self.redis.delete(
            f"verify:{user_id}"
        )