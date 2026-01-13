from src.interfaces.bot.ports.telegram_sender_impl import TelegramSenderImpl


async def get_telegram_sender_impl() -> TelegramSenderImpl:
    return TelegramSenderImpl()