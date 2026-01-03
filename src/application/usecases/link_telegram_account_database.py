from src.domain.repositories.user_repository import UserRepository

from src.common.logging.logger_main import logger


class LinkTelegramAccountDatabaseUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self,
        user_id: int,
        telegram_id: int,
        telegram_username: str | None,
    ) -> None:
        if not telegram_username:
            raise ValueError("Telegram username is required")

        if not isinstance(telegram_id, int):
            raise ValueError("Telegram ID must be an integer")

        await self.user_repository.set_telegram_id(
            user_id=user_id,
            telegram_id=telegram_id
        )

        await self.user_repository.set_telegram_username(
            user_id=user_id,
            telegram_username=telegram_username
        )

        logger.info(
            f"Telegram account linked: user_id={user_id}, tg_id={telegram_id}"
        )
