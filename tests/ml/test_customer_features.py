from pathlib import Path

from pipelines.analytics.customer_features import CustomerFeatures
from pipelines.warehouse.database_config import Database


def create_test_database(database_path: Path) -> Database:
    database = Database(database_path)

    database.create_schema("analytics")

    database.execute("""
        CREATE TABLE analytics.customer_metrics (
            customer_unique_id VARCHAR,
            total_orders INTEGER,
            total_items INTEGER,
            total_spent DOUBLE,
            average_order_value DOUBLE,
            first_order_date DATE,
            last_order_date DATE,
            customer_lifetime_days INTEGER
        )
    """)

    database.execute("""
        CREATE TABLE analytics.customer_rfm (
            customer_unique_id VARCHAR,
            recency INTEGER,
            frequency INTEGER,
            monetary DOUBLE,
            recency_score INTEGER,
            frequency_score INTEGER,
            monetary_score INTEGER,
            rfm_score INTEGER,
            segment VARCHAR
        )
    """)

    database.execute("""
        INSERT INTO analytics.customer_metrics VALUES
            (
                'U1',
                5,
                8,
                1000.00,
                200.00,
                '2024-01-10',
                '2024-06-10',
                152
            ),
            (
                'U2',
                2,
                3,
                300.00,
                150.00,
                '2024-03-15',
                '2024-05-20',
                66
            )
    """)

    database.execute("""
        INSERT INTO analytics.customer_rfm VALUES
            (
                'U1',
                10,
                5,
                1000.00,
                5,
                4,
                5,
                14,
                'Champions'
            ),
            (
                'U2',
                31,
                2,
                300.00,
                3,
                2,
                2,
                7,
                'Potential Loyalists'
            )
    """)

    return database


def test_customer_features_should_be_created(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    features = CustomerFeatures(database)
    features.build()

    result = database.query("""
        SELECT
            customer_unique_id,
            total_orders,
            total_items,
            total_spent,
            recency,
            frequency,
            monetary,
            rfm_score,
            segment
        FROM analytics.customer_features
        ORDER BY customer_unique_id
    """)

    assert result == [
        (
            "U1",
            5,
            8,
            1000.00,
            10,
            5,
            1000.00,
            14,
            "Champions",
        ),
        (
            "U2",
            2,
            3,
            300.00,
            31,
            2,
            300.00,
            7,
            "Potential Loyalists",
        ),
    ]
