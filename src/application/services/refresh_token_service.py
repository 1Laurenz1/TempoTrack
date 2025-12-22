from datetime import datetime, timedelta, timezone

import secrets
import hashlib


class RefreshTokenService:
    TOKEN_LENGTH = 64
    REFRESH_TOKEN_TTL_DAYS = 30
    
    def create_refresh_token(
        self,
    ) -> str:
        return secrets.token_urlsafe(self.TOKEN_LENGTH)
    
    def hash(
        self,
        token: str
    ) -> bytes:
        return hashlib.sha256(token.encode("utf-8")).digest()
    
    def get_expiration(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(days=self.REFRESH_TOKEN_TTL_DAYS)