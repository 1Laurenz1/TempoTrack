from pydantic import EmailStr

from src.domain.entities.user import User

from abc import ABC, abstractmethod
from typing import Optional


class UserRepository(ABC):
    
    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        """Return user by their email. Returns None if not found."""
        ...
        
    @abstractmethod
    def add(self, user: User) -> Optional[User]:
        """Add a new user to the database. Returns the created User or None if failed."""
        ...