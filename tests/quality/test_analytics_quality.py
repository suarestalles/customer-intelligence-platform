from pathlib import Path

from pipelines.quality.checks import (
    analytics_quality_checks,
    customer_metrics_dates_valid,
    customer_metrics_lifetime_valid,
    order_metrics_match_raw_orders,
    order_metrics_revenue_matches_raw_payments,
    rfm_score_consistent,
    rfm_scores_valid,
    rfm_segments_valid,
)
from pipelines.warehouse.database_config import Database


def create_analytics_database(tmp_path: Path) -> Database:
    database_path = tmp_path / "warehouse" / "quality.duckdb"
    database = Database(database_path)

    database.execute(
        """
        CREATE SCHEMA raw;
        CREATE SCHEMA analytics;

        CREATE TABLE raw.orders (
            order_id VARCHAR,
            customer_id VARCHAR
        );

        CREATE TABLE raw.order_payments (
            order_id VARCHAR,
            payment_value DECIMAL(10, 2)
        );

        CREATE TABLE analytics.order_metrics (
            order_id VARCHAR,
            customer_id VARCHAR,
            order_status VARCHAR,
            order_purchase_timestamp TIMESTAMP,
            order_approved_at TIMESTAMP,
            order_delivered_carrier_date TIMESTAMP,
            order_delivered_customer_date TIMESTAMP,
            order_estimated_delivery_date TIMESTAMP,
            total_items BIGINT,
            product_value DOUBLE,
            freight_value DOUBLE,
            payment_value DOUBLE
        );

        CREATE TABLE analytics.customer_metrics (
            customer_unique_id VARCHAR,
            total_orders INTEGER,
            total_items INTEGER,
            total_spent DECIMAL(18, 2),
            average_order_value DECIMAL(18, 2),
            first_order_date TIMESTAMP,
            last_order_date TIMESTAMP,
            customer_lifetime_days INTEGER
        );

        CREATE TABLE analytics.customer_rfm (
            customer_unique_id VARCHAR,
            recency INTEGER,
            frequency INTEGER,
            monetary DECIMAL(18, 2),
            recency_score INTEGER,
            frequency_score INTEGER,
            monetary_score INTEGER,
            rfm_score INTEGER,
            segment VARCHAR
        );
        """
    )

    database.execute(
        """
        INSERT INTO raw.orders VALUES
            ('order-1', 'customer-1'),
            ('order-2', 'customer-2');

        INSERT INTO raw.order_payments VALUES
            ('order-1', 165.00),
            ('order-2', 200.00);

        INSERT INTO analytics.order_metrics VALUES
            (
                'order-1',
                'customer-1',
                'delivered',
                '2024-01-01 10:00:00',
                '2024-01-01 11:00:00',
                '2024-01-02 10:00:00',
                '2024-01-05 10:00:00',
                '2024-01-10 10:00:00',
                1,
                90.00,
                10.00,
                100.00
            ),
            (
                'order-2',
                'customer-2',
                'delivered',
                '2024-01-02 10:00:00',
                '2024-01-02 11:00:00',
                '2024-01-03 10:00:00',
                '2024-01-06 10:00:00',
                '2024-01-11 10:00:00',
                1,
                180.00,
                20.00,
                200.00
            );

        INSERT INTO analytics.customer_metrics VALUES
            (
                'unique-1',
                1,
                2,
                165.00,
                165.00,
                '2026-01-01 10:00:00',
                '2026-01-01 10:00:00',
                0
            ),
            (
                'unique-2',
                1,
                1,
                200.00,
                200.00,
                '2026-01-02 10:00:00',
                '2026-01-02 10:00:00',
                0
            );

        INSERT INTO analytics.customer_rfm VALUES
            (
                'unique-1',
                10,
                1,
                165.00,
                3,
                3,
                3,
                9,
                'Potential Loyalists'
            ),
            (
                'unique-2',
                0,
                2,
                200.00,
                5,
                4,
                5,
                14,
                'Champions'
            );
        """
    )

    return database


def test_order_metrics_should_match_raw_orders(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = order_metrics_match_raw_orders(database)

    assert result.passed is True


def test_order_metrics_should_match_raw_revenue(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = order_metrics_revenue_matches_raw_payments(database)

    assert result.passed is True


def test_order_metrics_should_fail_when_order_is_missing(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        DELETE FROM analytics.order_metrics
        WHERE order_id = 'order-2';
        """
    )

    result = order_metrics_match_raw_orders(database)

    assert result.passed is False
    assert result.details["raw_orders"] == 2
    assert result.details["metric_orders"] == 1


def test_order_metrics_should_fail_when_revenue_differs(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        UPDATE analytics.order_metrics
        SET payment_value = 999.00
        WHERE order_id = 'order-1';
        """
    )

    result = order_metrics_revenue_matches_raw_payments(database)

    assert result.passed is False


def test_customer_dates_should_be_valid(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = customer_metrics_dates_valid(database)

    assert result.passed is True


def test_customer_dates_should_fail_when_reversed(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        UPDATE analytics.customer_metrics
        SET first_order_date = '2026-02-01',
            last_order_date = '2026-01-01'
        WHERE customer_unique_id = 'unique-1';
        """
    )

    result = customer_metrics_dates_valid(database)

    assert result.passed is False
    assert result.details["invalid_count"] == 1


def test_customer_lifetime_should_be_valid(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = customer_metrics_lifetime_valid(database)

    assert result.passed is True


def test_customer_lifetime_should_fail_when_negative(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        UPDATE analytics.customer_metrics
        SET customer_lifetime_days = -1
        WHERE customer_unique_id = 'unique-1';
        """
    )

    result = customer_metrics_lifetime_valid(database)

    assert result.passed is False
    assert result.details["invalid_count"] == 1


def test_rfm_scores_should_be_valid(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = rfm_scores_valid(database)

    assert result.passed is True


def test_rfm_scores_should_fail_for_invalid_score(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        UPDATE analytics.customer_rfm
        SET monetary_score = 10
        WHERE customer_unique_id = 'unique-1';
        """
    )

    result = rfm_scores_valid(database)

    assert result.passed is False
    assert result.details["invalid_count"] == 1


def test_rfm_score_should_be_consistent(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = rfm_score_consistent(database)

    assert result.passed is True


def test_rfm_score_should_fail_when_inconsistent(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        UPDATE analytics.customer_rfm
        SET rfm_score = 1
        WHERE customer_unique_id = 'unique-1';
        """
    )

    result = rfm_score_consistent(database)

    assert result.passed is False
    assert result.details["invalid_count"] == 1


def test_rfm_segments_should_be_valid(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    result = rfm_segments_valid(database)

    assert result.passed is True


def test_rfm_segments_should_fail_for_unknown_segment(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    database.execute(
        """
        UPDATE analytics.customer_rfm
        SET segment = 'Unknown Segment'
        WHERE customer_unique_id = 'unique-1';
        """
    )

    result = rfm_segments_valid(database)

    assert result.passed is False
    assert result.details["invalid_count"] == 1


def test_analytics_quality_suite_should_pass(
    tmp_path: Path,
) -> None:
    database = create_analytics_database(tmp_path)

    results = analytics_quality_checks(database)

    assert results

    for result in results:
        print(f"\n[{result.passed}] {result.name}: {result.message}")

        if not result.passed:
            print("DETAILS:", result.details)

    assert all(result.passed for result in results)
