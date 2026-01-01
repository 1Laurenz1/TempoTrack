from abc import ABC, abstractmethod


class TelegramSender(ABC):
    @abstractmethod
    async def send_verififaction_code(
        self,
        user_id: int,
        code: str
    ) -> None:
        ...