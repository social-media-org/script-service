"""Configuration service using Pydantic Settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Script Generation Service"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    # API
    api_v1_prefix: str = "/api/v1"
    allowed_hosts: list[str] = ["*"]
    app_port: int = 8000

    # MongoDB (keep for compatibility, but won't be used)
    mongodb_url: str = "mongodb://localhost:27017"
    DB_NAME: str = "fastapi_db"
    mongodb_min_pool_size: int = 10
    mongodb_max_pool_size: int = 100

    # Logging
    log_level: str = "INFO"
    log_format: str = "text"  # json or text

    # LLM API Keys
    deepseek_api_key: str = ""
    openai_api_base: str = "https://api.deepseek.com/v1"  # DeepSeek endpoint
    openai_model: str = "deepseek-chat"  # Default model

    # Transcription
    assemblyai_api_key: str = ""

    # Script generation defaults
    default_duration: int = 30  # seconds
    default_nb_sections: int = 1


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern).

    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Export singleton instance
settings = get_settings()
