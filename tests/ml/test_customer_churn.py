from pathlib import Path

from pipelines.ml.customer_churn import CustomerChurn
from pipelines.warehouse.database_config import Database


def test_customer_churn_should_be_created(tmp_path: Path) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = Database(database_path)

    database.create_schema("analytics")

    database.execute("""
        CREATE TABLE analytics.customer_features (
            customer_unique_id VARCHAR,
            total_orders INTEGER,
            total_items INTEGER,
            total_spent DECIMAL(10, 2),
            average_order_value DECIMAL(10, 2),
            first_order_date DATE,
            last_order_date DATE,
            customer_lifetime_days INTEGER,
            recency INTEGER,
            frequency INTEGER,
            monetary DECIMAL(10, 2),
            recency_score INTEGER,
            frequency_score INTEGER,
            monetary_score INTEGER,
            rfm_score INTEGER,
            segment VARCHAR
        )
    """)

    database.execute("""
        INSERT INTO analytics.customer_features VALUES
            (
                'C1',
                5,
                8,
                500.00,
                100.00,
                '2024-01-01',
                '2024-05-01',
                121,
                30,
                5,
                500.00,
                5,
                5,
                5,
                15,
                'Champions'
            ),
            (
                'C2',
                3,
                4,
                300.00,
                100.00,
                '2024-01-01',
                '2024-02-01',
                31,
                90,
                3,
                300.00,
                3,
                3,
                3,
                9,
                'Potential Loyalists'
            ),
            (
                'C3',
                2,
                2,
                150.00,
                75.00,
                '2024-01-01',
                '2024-01-01',
                0,
                91,
                2,
                150.00,
                2,
                2,
                2,
                6,
                'At Risk'
            ),
            (
                'C4',
                1,
                1,
                50.00,
                50.00,
                '2024-01-01',
                '2023-01-01',
                0,
                180,
                1,
                50.00,
                1,
                1,
                1,
                3,
                'Lost'
            )
    """)

    churn = CustomerChurn(database)

    churn.build()

    result = database.query("""
        SELECT
            customer_unique_id,
            recency,
            churn
        FROM analytics.customer_churn
        ORDER BY customer_unique_id
    """)

    assert result == [
        ("C1", 30, 0),
        ("C2", 90, 0),
        ("C3", 91, 1),
        ("C4", 180, 1),
    ]
