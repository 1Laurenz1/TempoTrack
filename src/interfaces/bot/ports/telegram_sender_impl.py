from aiogram import Bot

from src.interfaces.bot.bot_init import bot

from src.application.ports.telegram_sender import TelegramSender

from src.infrastructure.redis.redis_client import get_redis_connection
from src.infrastructure.redis.verification_code_storage import RedisVerificationCodeStorage

from src.common.logging.logger_main import logger

from redis.asyncio import Redis


class TelegramSenderImpl(TelegramSender):
    def __init__(
        self,
        bot: Bot = bot,
        redis: Redis | None = None,
    ):
        self.bot = bot
        self.redis = redis or get_redis_connection()
        
        
    async def send_verififaction_code(
        self,
        user_id: int,
        username: str,
        code: str
    ) -> None:
        telegram_id = await self.redis.get(
            name=f"tg:username:{username}"
        )

        if not telegram_id:
            raise ValueError("User never interacted with bot")

        chat_obj = await self.bot.get_chat(chat_id=int(telegram_id))
        chat_id = chat_obj.id
        
        await self.bot.send_message(
            chat_id=chat_id,
            text="You’re almost done linking your account.\n\n"
                "🔐 Your verification code:\n"
                f"<b>{code}</b>\n\n"
                "Enter this code on the website to confirm your Telegram account.\n\n"
                "⚠️ The code is valid for a limited time.\n"
                "If you didn’t request this, you can safely ignore this message."

        )
        
        key_for_tg_id = f"user:user_id:{user_id}"
        await self.redis.set(
            name=key_for_tg_id,
            value=telegram_id
        )
        logger.debug(f"A new value was written to Redis: {key_for_tg_id}/{telegram_id}")
        
        key_for_username = f"tg:id:{telegram_id}"
        await self.redis.set(
            name=key_for_username,
            value=username
        )
        logger.debug(f"A new value was written to Redis: {key_for_username}/{telegram_id}")
        
        logger.info(f"Message was sent succesffully to chat_id: {chat_id}(user_id: {user_id})")
        

    async def send_success_verification_message(
        self,
        user_id: int,
        username: str
    ) -> None:
        telegram_id = await self.redis.get(
            name=f"tg:username:{username}"
        )

        if not telegram_id:
            raise ValueError("User never interacted with bot")

        chat_obj = await self.bot.get_chat(chat_id=int(telegram_id))
        chat_id = chat_obj.id
        
        await self.bot.send_message(
            chat_id=chat_id,
            text="✅ <b>Verification completed successfully!</b>\n\n"
                "Your Telegram account is now linked to <b>TempoTrack</b>.\n\n"
                "⏰ You’ll receive <b>schedule-based notifications</b> and "
                "<b>reminders</b> here — exactly at the times you’ve set.\n\n"
                "<i>You’re all set!</i>"
        )
        
        logger.info(
            f"A message confirming successful verification has been sent to chat_id: {chat_id}"
            f"user_id({user_id})"
        )