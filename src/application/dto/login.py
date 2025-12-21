from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class LoginUserRequest:
    password: str
    email: Optional[str] = None
    username: Optional[str] = None

    def __post_init__(self):
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")


@dataclass(slots=True)
class LoginUserResponse:
    email: Optional[str]
    username: Optional[str]