from datetime import date
from pathlib import Path

from pipelines.ml.churn_dataset import ChurnDataset
from pipelines.warehouse.database_config import Database


def create_test_database(database_path: Path) -> Database:
    database = Database(database_path)

    database.create_schema("raw")

    database.execute("""
        CREATE TABLE raw.customers (
            customer_id VARCHAR,
            customer_unique_id VARCHAR
        )
    """)

    database.execute("""
        CREATE TABLE raw.orders (
            order_id VARCHAR,
            customer_id VARCHAR,
            order_purchase_timestamp TIMESTAMP
        )
    """)

    database.execute("""
        INSERT INTO raw.customers VALUES
            ('C1', 'U1'),
            ('C2', 'U2'),
            ('C3', 'U3')
    """)

    database.execute("""
        INSERT INTO raw.orders VALUES
            ('O1', 'C1', '2024-01-10 10:00:00'),
            ('O2', 'C1', '2024-02-10 10:00:00'),
            ('O3', 'C1', '2024-04-15 10:00:00'),

            ('O4', 'C2', '2024-01-15 10:00:00'),
            ('O5', 'C2', '2024-02-15 10:00:00'),

            ('O6', 'C3', '2024-05-01 10:00:00')
    """)

    return database


def test_churn_dataset_should_be_created(tmp_path: Path) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    dataset = ChurnDataset(
        database,
        prediction_window_days=90,
    )

    dataset.build()

    result = database.query("""
        SELECT
            customer_unique_id,
            total_orders,
            first_order_date,
            last_order_date,
            customer_lifetime_days,
            recency,
            churn
        FROM analytics.customer_churn_dataset
        ORDER BY customer_unique_id
    """)

    assert result == [
        (
            "U1",
            2,
            date(2024, 1, 10),
            date(2024, 2, 10),
            31,
            81,
            0,
        ),
        (
            "U2",
            2,
            date(2024, 1, 15),
            date(2024, 2, 15),
            31,
            76,
            1,
        ),
    ]


def test_churn_dataset_should_not_include_customers_without_history(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    dataset = ChurnDataset(database)

    dataset.build()

    result = database.query("""
        SELECT customer_unique_id
        FROM analytics.customer_churn_dataset
        ORDER BY customer_unique_id
    """)

    assert result == [
        ("U1",),
        ("U2",),
    ]
