from dataclasses import dataclass

from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class UserMeResponse():
    id: int
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    tg_username: str | None
    created_at: datetime