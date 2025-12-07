from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: SecretStr
    
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="UTF-8",
        extra="forbid"
    )
    
    
settings = Settings()