from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone


@dataclass
class User:
    id: Optional[int] = None
    username: Optional[str] = field(default_factory=str)
    email: Optional[str] = None
    password: str = field(default_factory=str)
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_username: Optional[str] = None
    telegram_id: Optional[int] = None
    
    schedules_count: int = 0
    main_schedule: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=datetime.now(timezone.utc))
    
    
    @property
    def is_active(self) -> bool:
        return self.schedules_count > 0
    
    @property
    def info_about_user(self) -> str:
        return f'{self.username} {self.email} {self.tg_username} {self.telegram_id}: {self.schedules_count}, {self.main_schedule}'