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
            recency_score,
            frequency_score,
            monetary_score,
            rfm_score,
            segment
        FROM analytics.customer_rfm
        ORDER BY customer_unique_id
        """
    )

    assert len(result) == 3

    customer1 = result[0]
    customer2 = result[1]
    customer3 = result[2]

    assert customer1[0] == "customer-1"
    assert customer1[1] == 0
    assert customer1[2] == 10
    assert float(customer1[3]) == 1000.00

    assert customer2[0] == "customer-2"
    assert customer2[1] == 31
    assert customer2[2] == 5
    assert float(customer2[3]) == 500.00

    assert customer3[0] == "customer-3"
    assert customer3[1] == 212
    assert customer3[2] == 1
    assert float(customer3[3]) == 50.00

    for row in result:
        recency_score = row[4]
        frequency_score = row[4]
        monetary_score = row[4]
        rfm_score = row[7]
        segment = row[8]

        assert 1 <= recency_score <= 5
        assert 1 <= frequency_score <= 5
        assert 1 <= monetary_score <= 5

        assert rfm_score == (recency_score + frequency_score + monetary_score)

        assert 3 <= rfm_score <= 15

        assert segment in {
            "Champions",
            "Loyal Customers",
            "Potential Loyalists",
            "At Risk",
            "Lost",
        }
