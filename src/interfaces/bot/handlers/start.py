from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.common.logging.logger_main import logger

from src.interfaces.bot.utils.get_info_user import get_info_about_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    #TODO: Send verification code
    
    user_info = get_info_about_user(message)
    
    code = 123456
    
    await message.answer(
        "👋 Hi! This is TempoTrack.\n\n"
        "You’re almost done linking your account.\n\n"
        "🔐 Your verification code:\n"
        f"<b>{code}</b>\n\n"
        "Enter this code on the website to confirm your Telegram account.\n\n"
        "⚠️ The code is valid for a limited time.\n"
        "If you didn’t request this, you can safely ignore this message."
    )

    
    logger.info(f"User {user_info.username}({user_info.tg_id}) started the bot")