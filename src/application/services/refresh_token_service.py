import secrets
import hashlib


class RefreshTokenService:
    TOKEN_LENGTH = 64
    
    def create_refresh_token(
        self,
    ) -> str:
        return secrets.token_urlsafe(self.TOKEN_LENGTH)
    
    def hash(
        self,
        token: str
    ) -> bytes:
        return hashlib.sha256(token.encode("utf-8")).digest()