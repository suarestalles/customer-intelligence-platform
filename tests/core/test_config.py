from pathlib import Path

from app.core.config import settings


def test_default_settings() -> None:
    assert settings.app_name == "Customer Intelligence Platform"
    assert settings.version == "0.1.0"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.database_path == Path("data/warehouse/customer_intelligence.duckdb")
