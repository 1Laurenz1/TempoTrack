from src.application.ports.telegram_indetify_storage import (
    TelegramIdentityStorage
)
from src.application.ports.telegram_sender import TelegramSender

from src.domain.repositories.user_repository import UserRepository

from src.common.logging.logger_main import logger


class LinkTelegramAccountDatabaseUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        storage: TelegramIdentityStorage,
        sender: TelegramSender,
    ):
        self.user_repository = user_repository
        self.storage = storage
        self.sender = sender

    async def execute(
        self,
        user_id: int,
    ) -> None:
        telegram_id = await self.storage.get_telegram_id_by_user_id(user_id)
        telegram_username = await self.storage.get_telegram_username_by_user_id(user_id)
        
        if not telegram_username:
            raise ValueError("Telegram username is required")

        await self.user_repository.set_telegram_id(
            user_id=user_id,
            telegram_id=telegram_id
        )

        await self.user_repository.set_telegram_username(
            user_id=user_id,
            telegram_username=telegram_username
        )
        
        await self.sender.send_success_verification_message(
            user_id=user_id,
            username=telegram_username
        )

        logger.info(
            f"Telegram account linked: user_id={user_id}, tg_id={telegram_id}"
        )
