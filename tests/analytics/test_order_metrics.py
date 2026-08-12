from pathlib import Path

from pipelines.analytics.order_metrics import OrderMetrics
from pipelines.warehouse.database_config import Database


def test_order_metrics_should_aggregate_order_data(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = Database(database_path)

    database.execute(
        """
        CREATE SCHEMA raw;

        CREATE TABLE raw.orders (
            order_id VARCHAR,
            customer_id VARCHAR,
            order_status VARCHAR,
            order_purchase_timestamp TIMESTAMP,
            order_approved_at TIMESTAMP,
            order_delivered_carrier_date TIMESTAMP,
            order_delivered_customer_date TIMESTAMP,
            order_estimated_delivery_date TIMESTAMP
        );

        CREATE TABLE raw.order_items (
            order_id VARCHAR,
            order_item_id INTEGER,
            price DECIMAL(10, 2),
            freight_value DECIMAL(10, 2)
        );

        CREATE TABLE raw.order_payments (
            order_id VARCHAR,
            payment_value DECIMAL(10, 2)
        );
        """
    )

    database.execute(
        """
        INSERT INTO raw.orders VALUES
        (
            'order-1',
            'customer-1',
            'delivered',
            '2026-01-01 10:00:00',
            NULL,
            NULL,
            NULL,
            NULL
        ),
        (
            'order-2',
            'customer-2',
            'delivered',
            '2026-01-02 10:00:00',
            NULL,
            NULL,
            NULL,
            NULL
        );
        """
    )

    database.execute(
        """
        INSERT INTO raw.order_items VALUES
            ('order-1', 1, 100.00, 10.00),
            ('order-1', 2, 50.00, 5.00),
            ('order-2', 1, 200.00, 20.00);
        """
    )

    database.execute(
        """
        INSERT INTO raw.order_payments VALUES
            ('order-1', 100.00),
            ('order-1', 65.00),
            ('order-2', 200.00);
        """
    )

    metrics = OrderMetrics(database)

    metrics.build()

    result = database.query("""
        SELECT
            order_id,
            total_items,
            product_value,
            freight_value,
            payment_value
        FROM analytics.order_metrics
    """)

    assert result == [
        (
            "order-1",
            2,
            150.00,
            15.00,
            165.00,
        ),
        (
            "order-2",
            1,
            200.00,
            20.00,
            200.00,
        ),
    ]
