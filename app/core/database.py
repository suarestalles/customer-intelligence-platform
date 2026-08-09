from app.core.config import settings
from pipelines.warehouse.database_config import Database


def get_database() -> Database:
    return Database(settings.database_path)
