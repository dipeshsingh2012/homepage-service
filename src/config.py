from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8002
    CONTENTFUL_SPACE_ID: Optional[str] = None
    CONTENTFUL_ACCESS_TOKEN: Optional[str] = None
    CONTENTFUL_ENVIRONMENT: str = "master"
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
