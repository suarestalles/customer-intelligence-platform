import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "Customer Intelligence Platform")
    version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    database_path: Path = Path(
        os.getenv("DATABASE_PATH", "data/warehouse/customer_intelligence.duckdb")
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Setting()
