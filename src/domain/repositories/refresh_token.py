from abc import ABC, abstractmethod

from src.domain.entities.refresh_token import RefreshToken

from typing import Optional


class RefreshTokenRepository(ABC):
    @abstractmethod
    async def add(self, refresh_token: RefreshToken) -> Optional[RefreshToken]:
        """Adds a refresh token to the database and returns it"""
        ...
    
    @abstractmethod
    async def get_by_hash(self, token_hash: bytes) -> Optional[RefreshToken]:
        """Returns the refresh token by hash or None if not found."""
        ...