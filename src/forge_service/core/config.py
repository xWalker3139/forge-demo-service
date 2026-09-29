from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field

enable_fault_injection: bool = False


class Settings(BaseSettings):
    app_name: str = "Forge Demo Service"
    app_version: str = "0.1.0"
    environment: str = "local"
    log_level: str = "INFO"
    enable_fault_injection: bool = False

    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    graceful_shutdown_timeout_seconds: int = Field(
        default=30,
        ge=1,
        le=300,
    )

    model_config = SettingsConfigDict(
        env_prefix="FORGE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
