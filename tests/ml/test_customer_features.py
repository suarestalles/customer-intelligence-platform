from datetime import date
from decimal import Decimal
from pathlib import Path

from pipelines.ml.customer_features import CustomerFeatures
from pipelines.warehouse.database_config import Database


def create_test_database(database_path: Path) -> Database:
    database = Database(database_path)

    database.execute(
        """
        CREATE SCHEMA raw;

        CREATE TABLE raw.customers (
            customer_id VARCHAR,
            customer_unique_id VARCHAR
        );

        CREATE TABLE raw.orders (
            order_id VARCHAR,
            customer_id VARCHAR,
            order_purchase_timestamp TIMESTAMP
        );

        CREATE TABLE raw.order_items (
            order_id VARCHAR,
            order_item_id INTEGER,
            price DECIMAL(10, 2),
            freight_value DECIMAL(10, 2)
        );
        """
    )

    database.execute(
        """
        INSERT INTO raw.customers VALUES
            ('customer-1', 'unique-1'),
            ('customer-2', 'unique-2'),
            ('customer-3', 'unique-3');
        """
    )

    database.execute(
        """
        INSERT INTO raw.orders VALUES
            (
                'order-1',
                'customer-1',
                '2024-01-01 10:00:00'
            ),
            (
                'order-2',
                'customer-1',
                '2024-02-01 10:00:00'
            ),
            (
                'order-3',
                'customer-1',
                '2024-04-15 10:00:00'
            ),
            (
                'order-4',
                'customer-2',
                '2024-03-01 10:00:00'
            ),
            (
                'order-5',
                'customer-2',
                '2024-06-30 10:00:00'
            ),
            (
                'order-6',
                'customer-3',
                '2024-02-15 10:00:00'
            );
        """
    )

    database.execute(
        """
        INSERT INTO raw.order_items VALUES
            ('order-1', 1, 100.00, 10.00),
            ('order-1', 2, 50.00, 5.00),
            ('order-2', 1, 200.00, 20.00),
            ('order-3', 1, 999.00, 99.00),
            ('order-4', 1, 80.00, 8.00),
            ('order-5', 1, 500.00, 50.00),
            ('order-6', 1, 120.00, 12.00);
        """
    )

    return database


def test_customer_features_should_use_historical_orders(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()

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
            customer_lifetime_days,
            recency,
            frequency,
            monetary
        FROM analytics.customer_features
        ORDER BY customer_unique_id
        """
    )

    assert result == [
        (
            "unique-1",
            2,
            3,
            Decimal("350.00"),
            175.0,
            date(2024, 1, 1),
            date(2024, 2, 1),
            31,
            60,
            2,
            Decimal("350.00"),
        ),
        (
            "unique-2",
            1,
            1,
            Decimal("80.00"),
            80.0,
            date(2024, 3, 1),
            date(2024, 3, 1),
            0,
            31,
            1,
            Decimal("80.00"),
        ),
        (
            "unique-3",
            1,
            1,
            Decimal("120.00"),
            120.0,
            date(2024, 2, 15),
            date(2024, 2, 15),
            0,
            46,
            1,
            Decimal("120.00"),
        ),
    ]


def test_customer_features_should_have_unique_customers(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()

    duplicates = database.query(
        """
        SELECT
            customer_unique_id,
            COUNT(*) AS row_count
        FROM analytics.customer_features
        GROUP BY customer_unique_id
        HAVING COUNT(*) > 1
        """
    )

    assert duplicates == []


def test_customer_features_should_ignore_future_orders(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()

    result = database.query(
        """
        SELECT
            total_orders,
            total_items,
            total_spent
        FROM analytics.customer_features
        WHERE customer_unique_id = 'unique-1'
        """
    )

    assert result == [
        (
            2,
            3,
            350.00,
        )
    ]


def test_customer_features_should_not_duplicate_orders(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()

    result = database.query(
        """
        SELECT
            customer_unique_id,
            total_orders
        FROM analytics.customer_features
        ORDER BY customer_unique_id
        """
    )

    assert result == [
        ("unique-1", 2),
        ("unique-2", 1),
        ("unique-3", 1),
    ]
