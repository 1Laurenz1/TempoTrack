from pydantic import EmailStr

from src.domain.entities.user import User

from abc import ABC, abstractmethod
from typing import Optional


class UserRepository(ABC):
    
    @abstractmethod
    async def get_user_by_id(self, id: int) -> Optional[User]:
        """Returns a user by their id or None if not found"""
        ...
    
    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        """Return user by their email. Returns None if not found."""
        ...
        
    @abstractmethod
    async def get_user_by_login(self, login: str) -> Optional[User]:
        """Return user by their email or username. Returns None if not found."""
        ...
        
    @abstractmethod
    async def add(self, user: User) -> Optional[User]:
        """Add a new user to the database. Returns the created User or None if failed."""
        ...
        
    @abstractmethod
    async def increment_schedules_count(self, user_id: int) -> None:
        """Increases the user's schedules by 1"""
        ...
        
    @abstractmethod
    async def decrement_schedules_count(self, user_id: int) -> None:
        """Decremens the user's schedules by 1"""
        ...
        
    @abstractmethod
    async def set_main_schedule(self, user_id: int, schedule_id: int | None) -> None:
        """Sets the specified schedule_id in main_schedule for the user"""
        ...