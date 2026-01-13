from dataclasses import dataclass

from typing import Optional


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    username: str
    password: str
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(slots=True)
class RegisterUserResponse:
    email: str
    username: str
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None