from pathlib import Path

from pipelines.warehouse.database import Database
from pipelines.warehouse.loader import RawLoader

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIRECTORY = PROJECT_ROOT / "data" / "external" / "olist" / "raw"

DATABASE_PATH = PROJECT_ROOT / "data" / "warehouse" / "customer_intelligence.duckdb"


def main() -> None:
    database = Database(DATABASE_PATH)

    loader = RawLoader(database, RAW_DIRECTORY)

    loader.load_all()

    print("Raw data loaded successfully.")


if __name__ == "__main__":
    main()
