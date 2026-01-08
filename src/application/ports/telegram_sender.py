from abc import ABC, abstractmethod

from src.domain.entities.schedule_notification import ScheduleNotification


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
        
    
    @abstractmethod
    async def send_notification_message(
        self,
        user_id: int,
        username: str,
        notification: ScheduleNotification,
    ) -> None:
        ...