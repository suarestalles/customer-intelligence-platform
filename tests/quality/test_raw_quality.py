from pathlib import Path

from pipelines.quality.checks import (
    foreign_key_integrity,
    no_nulls,
    non_negative,
    raw_quality_checks,
    unique_column,
    unique_combination,
)
from pipelines.warehouse.database_config import Database


def create_raw_database(tmp_path: Path) -> Database:
    database_path = tmp_path / "warehouse" / "quality.duckdb"
    database = Database(database_path)

    database.execute(
        """
        CREATE SCHEMA raw;

        CREATE TABLE raw.customers (
            customer_id VARCHAR,
            customer_unique_id VARCHAR,
            customer_zip_code_prefix VARCHAR,
            customer_city VARCHAR,
            customer_state VARCHAR
        );

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
            product_id VARCHAR,
            seller_id VARCHAR,
            shipping_limit_date TIMESTAMP,
            price DECIMAL(18, 2),
            freight_value DECIMAL(18, 2)
        );

        CREATE TABLE raw.order_payments (
            order_id VARCHAR,
            payment_sequential INTEGER,
            payment_type VARCHAR,
            payment_installments INTEGER,
            payment_value DECIMAL(18, 2)
        );

        CREATE TABLE raw.products (
            product_id VARCHAR,
            product_category_name VARCHAR,
            product_name_lenght BIGINT,
            product_description_lenght BIGINT,
            product_photos_qty BIGINT,
            product_weight_g BIGINT,
            product_length_cm BIGINT,
            product_height_cm BIGINT,
            product_width_cm BIGINT
        );
        """
    )

    database.execute(
        """
        INSERT INTO raw.customers VALUES
            ('customer-1', 'unique-1', 74000, 'Goiania', 'GO'),
            ('customer-2', 'unique-2', 74001, 'Goiania', 'GO');

        INSERT INTO raw.orders VALUES
            (
                'order-1',
                'customer-1',
                'delivered',
                '2024-01-01 10:00:00',
                '2024-01-01 11:00:00',
                '2024-01-02 10:00:00',
                '2024-01-05 10:00:00',
                '2024-01-10 10:00:00'
            ),
            (
                'order-2',
                'customer-2',
                'delivered',
                '2024-01-02 10:00:00',
                '2024-01-02 11:00:00',
                '2024-01-03 10:00:00',
                '2024-01-06 10:00:00',
                '2024-01-11 10:00:00'
            );

        INSERT INTO raw.order_items VALUES
            (
                'order-1',
                1,
                'product-1',
                'seller-1',
                '2024-01-01 12:00:00',
                100.00,
                10.00
            ),
            (
                'order-1',
                2,
                'product-2',
                'seller-1',
                '2024-01-01 13:00:00',
                50.00,
                5.00
            ),
            (
                'order-2',
                1,
                'product-3',
                'seller-2',
                '2024-01-02 12:00:00',
                200.00,
                20.00
            );

        INSERT INTO raw.order_payments VALUES
            ('order-1', 1, 'credit_card', 2, 100.00),
            ('order-2', 1, 'credit_card', 3, 200.00);
        """
    )

    return database


def test_unique_column_should_pass(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    result = unique_column(
        database,
        "raw",
        "orders",
        "order_id",
    )

    assert result.passed is True


def test_unique_column_should_fail_for_duplicates(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    database.execute(
        """
        INSERT INTO raw.orders VALUES
            (
                'order-1',
                'customer-1',
                'delivered',
                '2026-01-03 10:00:00',
                '2026-01-03 10:00:00',
                '2026-01-03 10:00:00',
                '2026-01-03 10:00:00',
                '2026-01-03 10:00:00'
            );
        """
    )

    result = unique_column(
        database,
        "raw",
        "orders",
        "order_id",
    )

    assert result.passed is False
    assert result.details["total_rows"] == 3
    assert result.details["distinct_values"] == 2


def test_no_nulls_should_pass(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    result = no_nulls(
        database,
        "raw",
        "customers",
        "customer_id",
    )

    assert result.passed is True


def test_no_nulls_should_fail(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    database.execute(
        """
        INSERT INTO raw.customers VALUES
            (NULL, 'unique-1', 0, 'Serranópolis', 'GO'),
        """
    )

    result = no_nulls(
        database,
        "raw",
        "customers",
        "customer_id",
    )

    assert result.passed is False
    assert result.details["null_count"] == 1


def test_non_negative_should_pass(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    result = non_negative(
        database,
        "raw",
        "order_payments",
        "payment_value",
    )

    assert result.passed is True


def test_non_negative_should_fail(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    database.execute(
        """
        INSERT INTO raw.order_payments VALUES
            ('order-1', 1, 'credit_card', 2, -100.00);
        """
    )

    result = non_negative(
        database,
        "raw",
        "order_payments",
        "payment_value",
    )

    assert result.passed is False
    assert result.details["invalid_count"] == 1


def test_foreign_key_should_pass(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    result = foreign_key_integrity(
        database,
        "raw",
        "orders",
        "customer_id",
        "raw",
        "customers",
        "customer_id",
    )

    assert result.passed is True


def test_foreign_key_should_fail_for_orphan_records(
    tmp_path: Path,
) -> None:
    database = create_raw_database(tmp_path)

    database.execute(
        """
        INSERT INTO raw.orders VALUES
            (
                'order-1',
                'customer-1',
                'delivered',
                '2024-01-01 10:00:00',
                '2024-01-01 11:00:00',
                '2024-01-02 10:00:00',
                '2024-01-05 10:00:00',
                '2024-01-10 10:00:00'
            ),
        """
    )

    result = foreign_key_integrity(
        database,
        "raw",
        "orders",
        "customer_id",
        "raw",
        "customers",
        "customer_id",
    )

    assert result.passed is False
    assert result.details["orphan_count"] == 1


def test_unique_combination_should_pass(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    result = unique_combination(
        database,
        "raw",
        "order_items",
        ("order_id", "order_item_id"),
    )

    assert result.passed is True


def test_raw_quality_suite_should_pass(tmp_path: Path) -> None:
    database = create_raw_database(tmp_path)

    results = raw_quality_checks(database)

    assert results

    for result in results:
        print(f"\n[{result.passed}] {result.name}: {result.message}")

        if not result.passed:
            print("DETAILS:", result.details)

    assert all(result.passed for result in results)
