from aiogram.types import Message

from src.interfaces.bot.schemas.user_info import UserInfo

from src.common.logging.logger_main import logger


def get_info_about_user(message: Message) -> UserInfo:
    tg_id: str = getattr(message.from_user, "id", None)
    username: str = getattr(message.from_user, "username", "unknown_username")
    first_name: str = getattr(message.from_user, "first_name", "")
    last_name: str = getattr(message.from_user, "last_name", "")
    
    user_info = UserInfo(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    
    logger.info(f"Info about user {user_info} (tg_id: {user_info.tg_id} collected)")
    return user_info