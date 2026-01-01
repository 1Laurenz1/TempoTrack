from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from redis.asyncio import Redis

from src.common.logging.logger_main import logger

from src.interfaces.bot.utils.get_info_user import get_info_about_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    
    user_info = get_info_about_user(message)
    
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