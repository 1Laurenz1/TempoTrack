from abc import ABC, abstractmethod
from typing import Optional

class TelegramIdentityStorage(ABC):
    @abstractmethod
    async def get_telegram_id_by_user_id(
        self,
        user_id: int
    ) -> Optional[int]:
        ...
        
        
    @abstractmethod
    async def get_telegram_username_by_user_id(
        self,
        user_id: int
    ) -> Optional[str]:
        ...