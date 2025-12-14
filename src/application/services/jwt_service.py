import jwt
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from jwt.exceptions import PyJWTError

from src.infrastructure.config.config_reader import settings
from src.application.exceptions.auth import InvalidTokenError


@dataclass(slots=True)
class JwtService:
    secret_key: str
    algorithm: str
    access_token_ttl_minutes: int
    
    
    def create_access_token(self, payload: dict) -> str:
        to_encode = payload.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_ttl_minutes
        )
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

        
    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
        except PyJWTError as e:
            raise InvalidTokenError("Invalid or expired token") from e
        
        
jwt_service = JwtService(
    secret_key=settings.SECRET_KEY.get_secret_value(),
    algorithm=settings.ALGORITHM,
    access_token_ttl_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
