from abc import ABC, abstractmethod

class VerificationCodeStorage(ABC):
    @abstractmethod
    async def save(self, user_id: int, code: str, ttl_seconds: int) -> None:
        ...

    @abstractmethod
    async def get(self, user_id: int) -> str | None:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...