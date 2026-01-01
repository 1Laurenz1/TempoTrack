from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: SecretStr
    DEV_DATABASE_URL: SecretStr
    TEST_DATABASE_URL: SecretStr | None = None
    
    REDSIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    BOT_TOKEN: SecretStr
    
    SECRET_KEY: SecretStr
    ALGORITHM: SecretStr = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="UTF-8",
        extra="forbid"
    )
    
    
settings = Settings()