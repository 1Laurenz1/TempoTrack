from src.application.services.password_service import PasswordService
from src.application.services.refresh_token_service import RefreshTokenService
from src.application.services.jwt_service import JwtService

from src.infrastructure.config.config_reader import settings


def get_password_service() -> PasswordService:
    return PasswordService()


def get_refresh_token_service() -> RefreshTokenService:
    return RefreshTokenService()


def get_jwt_service() -> JwtService:
    return JwtService(
        secret_key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM.get_secret_value(),
        access_token_ttl_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )