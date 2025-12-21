from abc import ABC, abstractmethod

from src.domain.entities.refresh_token import RefreshToken

from typing import Optional


class RefreshTokenRepository(ABC):
    @abstractmethod
    async def exists_refresh_token(self, token_hash: bytes) -> Optional[RefreshToken]:
        """Checks if a refresh token exists in the database. Returns None if not found"""
        ...
    
    @abstractmethod
    async def add(self, refresh_token: RefreshToken) -> Optional[RefreshToken]:
        """Adds a refresh token to the database and returns it"""
        ...