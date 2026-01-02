from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from redis.asyncio import Redis

from src.infrastructure.redis.redis_client import get_redis_connection

from src.common.logging.logger_main import logger

from src.interfaces.bot.utils.get_info_user import get_info_about_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user_info = await get_info_about_user(message)
    redis = await get_redis_connection()
    
    key = f"tg:username:{user_info.username}"
    
    await redis.set(
        name=key,
        value=user_info.tg_id
    )
    logger.debug(
        f"A new value was written to Redis: {key}/{user_info.tg_id}"
    )
    
    await message.answer(
        "<b>👋 Hi! This is TempoTrack.</b>\n"
        "To link your Telegram account with your website account:"
        "1. Go to the website"
        "2. Click 'Verify Account'"
        "3. Enter your Telegram username"
        "4. You'll receive a verification code here\n"
        "<b>⚠️ Your username</b>: Laurenz5"
        "(Use this exact username on the website, without @)"
    )

    
    logger.info(f"User {user_info.username}({user_info.tg_id}) started the bot")