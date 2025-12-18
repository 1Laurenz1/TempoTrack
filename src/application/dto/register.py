from dataclasses import dataclass, field

from typing import Optional


@dataclass
class RegisterUserRequest:
    email: str = field(default_factory=str)
    username: str = field(default_factory=str)
    password: str = field(default_factory=str)
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None