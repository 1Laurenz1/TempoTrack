from abc import ABC, abstractmethod


class TelegramSender(ABC):
    @abstractmethod
    async def send_verififaction_code(
        self,
        user_id: int,
        username: str,
        code: str
    ) -> None:
        ...
        
        
    @abstractmethod
    async def send_success_verification_message(
        self,
        user_id: int,
        username: str
    ) -> None:
        ...