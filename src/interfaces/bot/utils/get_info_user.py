from aiogram.types import Message

from src.interfaces.bot.schemas.user_info import UserInfo

from src.common.logging.logger_main import logger


async def get_info_about_user(message: Message) -> UserInfo | None:
    tg_id: int = getattr(message.from_user, "id", None)
    username: str = getattr(message.from_user, "username", None)
    first_name: str = getattr(message.from_user, "first_name", "")
    last_name: str = getattr(message.from_user, "last_name", "")

    if not username:
        await message.answer(
            "❌ You don’t have a Telegram username.\n"
            "Please set a username in Telegram settings and try again."
        )
        logger.info(f"The user(user_id: {tg_id}) doesn't have a @username, returning...")
        return None  # важно вернуть None, чтобы хендлер знал

    user_info = UserInfo(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    
    logger.info(f"Info about user {user_info} (tg_id: {user_info.tg_id} collected)")
    return user_info
