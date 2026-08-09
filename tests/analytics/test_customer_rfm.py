from pathlib import Path

from pipelines.analytics.customer_rfm import CustomerRFM
from pipelines.warehouse.database_config import Database


def test_customer_rfm_should_generate_scores(tmp_path: Path) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = Database(database_path)

    database.execute(
        """
        CREATE SCHEMA analytics;

        CREATE TABLE analytics.customer_metrics (
            customer_unique_id VARCHAR,
            total_orders INTEGER,
            total_spent DECIMAL(10, 2),
            last_order_date TIMESTAMP
        );

        INSERT INTO analytics.customer_metrics VALUES
            (
                'customer-1',
                10,
                1000.00,
                '2026-08-01'
            ),
            (
                'customer-2',
                5,
                500.00,
                '2026-07-01'
            ),
            (
                'customer-3',
                1,
                50.00,
                '2026-01-01'
            );
        """
    )

    rfm = CustomerRFM(database)

    rfm.build()

    result = database.query(
        """
        SELECT
            customer_unique_id,
            recency,
            frequency,
            monetary,
            rfm_score,
            segment
        FROM analytics.customer_rfm
        ORDER BY customer_unique_id
        """
    )

    assert len(result) == 3

    for row in result:
        rfm_score = row[4]

        assert 3 <= rfm_score <= 15
        assert row[5] in {
            "Champions",
            "Loyal Customers",
            "Potential Loyalists",
            "At Risk",
            "Lost",
        }
