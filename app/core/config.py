from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "OpsBeacon"
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    git_commit: str = Field(default="local", alias="GIT_COMMIT")
    app_env: str = Field(default="development", alias="APP_ENV")
    database_url: str = Field(
        default="postgresql+psycopg://opsbeacon:opsbeacon@db:5432/opsbeacon",
        alias="DATABASE_URL",
    )
    http_timeout_seconds: float = Field(default=5.0, alias="HTTP_TIMEOUT_SECONDS")
    worker_interval_seconds: int = Field(default=60, alias="WORKER_INTERVAL_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
