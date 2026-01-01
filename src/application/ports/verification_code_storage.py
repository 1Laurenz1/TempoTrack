from abc import ABC, abstractmethod
from typing import Optional

class VerificationCodeStorage(ABC):
    @abstractmethod
    async def set_verification_code(
        self,
        user_id: int,
        code: str,
        ttl_seconds: int = 300    
    ) -> None:
        ...

    @abstractmethod
    async def get_verify_code_by_user_id(self, user_id: int) -> Optional[str]:
        ...

    @abstractmethod
    async def delete_code(self, user_id: int) -> None:
        ...