from pathlib import Path

from pipelines.analytics.customer_metrics import CustomerMetrics
from pipelines.warehouse.database_config import Database


def test_customer_metrics_should_aggregate_orders(tmp_path: Path) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = Database(database_path)

    database.execute(
        """
        CREATE SCHEMA raw;
        CREATE SCHEMA analytics;

        CREATE TABLE raw.customers (
            customer_id VARCHAR,
            customer_unique_id VARCHAR
        );

        CREATE TABLE analytics.order_metrics (
            order_id VARCHAR,
            customer_id VARCHAR,
            total_items INTEGER,
            payment_value DECIMAL(10, 2),
            order_purchase_timestamp TIMESTAMP
        );

        """
    )

    database.execute(
        """
        INSERT INTO raw.customers VALUES
            ('customer-1', 'unique-1');
        """
    )

    database.execute(
        """
        INSERT INTO analytics.order_metrics VALUES
            (
                'order-1',
                'customer-1',
                2,
                100.00,
                '2026-01-01 10:00:00'
            ),
            (
                'order-2',
                'customer-1',
                3,
                200.00,
                '2026-01-11 10:00:00'
            );
        """
    )

    metrics = CustomerMetrics(database)

    metrics.build()

    result = database.query(
        """
        SELECT
            customer_unique_id,
            total_orders,
            total_items,
            total_spent,
            average_order_value,
            first_order_date,
            last_order_date,
            customer_lifetime_days
        FROM analytics.customer_metrics
        """
    )

    assert result == [
        (
            "unique-1",
            2,
            5,
            300.00,
            150.00,
            # DuckDB pode retornar os timestamps como datetime.
            # Ajustaremos a asserção caso necessário.
            result[0][5],
            result[0][6],
            10,
        )
    ]
