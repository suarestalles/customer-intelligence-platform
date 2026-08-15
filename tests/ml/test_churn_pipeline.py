from pathlib import Path

from pipelines.ml.churn_pipeline import ChurnPipeline
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
        CREATE TABLE raw.order_items (
            order_id VARCHAR,
            order_item_id INTEGER,
            product_id VARCHAR,
            price DECIMAL(10, 2)
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

            ('O3', 'C2', '2024-01-15 10:00:00'),
            ('O4', 'C2', '2024-04-15 10:00:00'),

            ('O5', 'C3', '2024-05-01 10:00:00')
    """)

    database.execute("""
        INSERT INTO raw.order_items VALUES
            ('O1', 1, 'P1', 100.00),
            ('O1', 2, 'P2', 200.00),

            ('O2', 1, 'P3', 50.00),

            ('O3', 1, 'P4', 80.00),

            ('O4', 1, 'P5', 120.00),

            ('O5', 1, 'P6', 90.00)
    """)

    return database


def test_churn_pipeline_should_build_dataset(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    ChurnPipeline(database).build_dataset()

    customer_features = database.query("""
        SELECT
            customer_unique_id
        FROM analytics.customer_features
        ORDER BY customer_unique_id
    """)

    churn_dataset = database.query("""
        SELECT
            customer_unique_id
        FROM analytics.customer_churn_dataset
        ORDER BY customer_unique_id
    """)

    assert customer_features == [
        ("U1",),
        ("U2",),
    ]

    assert churn_dataset == [
        ("U1",),
        ("U2",),
    ]

    result = database.query("""
        SELECT
            customer_unique_id,
            total_orders,
            total_items,
            total_spent,
            frequency,
            monetary,
            churn
        FROM analytics.customer_churn_dataset
        ORDER BY customer_unique_id
    """)

    assert result == [
        (
            "U1",
            1,
            2,
            300.00,
            1,
            300.00,
            0,
        ),
        (
            "U2",
            1,
            1,
            80.00,
            1,
            80.00,
            0,
        ),
    ]
