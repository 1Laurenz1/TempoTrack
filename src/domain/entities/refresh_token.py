from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone


@dataclass
class RefreshToken:
    user_id: int
    token_hash: bytes
    expires_at: datetime    
    
    id: Optional[int] = None

    revoked: bool = False
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))