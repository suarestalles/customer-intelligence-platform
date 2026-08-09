from pathlib import Path

from pipelines.warehouse.database_config import Database
from pipelines.warehouse.loader import RawLoader


def test_loader_should_create_database_from_csv(tmp_path: Path) -> None:
    raw_directory = tmp_path / "raw"
    raw_directory.mkdir()

    customers_file = raw_directory / "olist_customers_dataset.csv"

    customers_file.write_text(
        """customer_id,customer_unique_id,customer_zip_code_prefix,customer_city,customer_state
1,customer-1,01000,sao paulo,SP
2,customer-2,20000,rio de janeiro,RJ
3,customer-3,30000,belo horizonte,MG
""",
        encoding="utf-8",
    )

    products_file = raw_directory / "olist_products_dataset.csv"
    products_file.write_text(
        """product_id,product_category_name,product_weight_g
product-1,health_beauty,500
product-2,computers,1000
""",
        encoding="utf-8",
    )

    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = Database(database_path)

    loader = RawLoader(database, raw_directory)

    loader.load_all()

    tables = database.query(
        """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'raw'
            ORDER BY table_name
        """
    )

    assert tables == [
        ("customers",),
        ("products",),
    ]
