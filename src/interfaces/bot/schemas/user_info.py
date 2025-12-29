from dataclasses import dataclass
from typing import Optional


@dataclass
class UserInfo:
    tg_id: Optional[int]
    username: str
    first_name: str
    last_name: Optional[str]