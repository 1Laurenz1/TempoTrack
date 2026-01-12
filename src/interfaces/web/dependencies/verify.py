from fastapi import Depends

from src.interfaces.bot.ports.telegram_sender_impl import TelegramSenderImpl

from src.infrastructure.redis.redis_client import get_redis_connection


async def get_telegram_sender_impl() -> TelegramSenderImpl:
    redis = await get_redis_connection()
    
    return TelegramSenderImpl(
        # redis=redis,
    )