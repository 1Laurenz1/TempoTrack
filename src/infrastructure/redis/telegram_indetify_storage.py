from redis.asyncio import Redis

from src.application.ports.telegram_indetify_storage import (
    TelegramIdentityStorage
)

from typing import Optional


class RedisTelegramIndetifyStorage(TelegramIdentityStorage):
    def __init__(self, redis: Redis):
        self.redis = redis
    
    async def get_telegram_id_by_user_id(
        self,
        user_id: int
    ) -> Optional[str]:
        telegram_id = await self.redis.get(
            name=f"user:user_id:{user_id}"
        )
        
        return int(telegram_id) if telegram_id else None
    
    
    async def get_telegram_username_by_user_id(
        self,
        user_id: int
    ) -> Optional[str]:
        telegram_id = await self.redis.get(
            name=f"user:user_id:{user_id}"
        )
        
        if telegram_id is None:
            return None
        
        tg_username = await self.redis.get(
            name=f"tg:id:{telegram_id}"
        )
        
        return str(tg_username) if tg_username else None