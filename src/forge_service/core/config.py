from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

enable_fault_injection: bool = False


class Settings(BaseSettings):
    app_name: str = "Forge Demo Service"
    app_version: str = "0.1.0"
    environment: str = "local"
    log_level: str = "INFO"
    enable_fault_injection: bool = False

    model_config = SettingsConfigDict(
        env_prefix="FORGE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
