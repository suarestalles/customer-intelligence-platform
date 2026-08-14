from datetime import date
from pathlib import Path

from pipelines.analytics.customer_cohorts import CustomerCohorts
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
        INSERT INTO raw.customers VALUES
            ('C1', 'U1'),
            ('C2', 'U2'),
            ('C3', 'U3')
    """)

    database.execute("""
        INSERT INTO raw.orders VALUES
            ('O1', 'C1', '2024-01-15 10:00:00'),
            ('O2', 'C1', '2024-02-10 11:00:00'),
            ('O3', 'C1', '2024-04-20 12:00:00'),
            ('O4', 'C2', '2024-03-05 09:00:00'),
            ('O5', 'C2', '2024-03-20 14:00:00'),
            ('O6', 'C2', '2024-05-10 15:00:00')
    """)

    return database


def test_customer_cohorts_should_be_created(tmp_path: Path) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    cohorts = CustomerCohorts(database)
    cohorts.build()

    result = database.query("""
        SELECT
            cohort_month,
            months_since_first_purchase,
            customers,
            retained_customers,
            retention_rate
        FROM analytics.customer_cohorts
        ORDER BY
            cohort_month,
            months_since_first_purchase
    """)

    assert result == [
        (date(2024, 1, 1), 0, 1, 1, 100.0),
        (date(2024, 1, 1), 1, 1, 1, 100.0),
        (date(2024, 1, 1), 3, 1, 1, 100.0),
        (date(2024, 3, 1), 0, 1, 1, 100.0),
        (date(2024, 3, 1), 2, 1, 1, 100.0),
    ]


def test_customer_cohorts_should_not_duplicate_same_month(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    cohorts = CustomerCohorts(database)
    cohorts.build()

    result = database.query("""
        SELECT
            cohort_month,
            months_since_first_purchase,
            customers,
            retained_customers
        FROM analytics.customer_cohorts
        WHERE cohort_month = DATE '2024-03-01'
          AND months_since_first_purchase = 0
    """)

    assert result == [
        (date(2024, 3, 1), 0, 1, 1),
    ]


def test_customer_cohorts_should_ignore_orders_without_purchase_date(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    cohorts = CustomerCohorts(database)

    cohorts.build()

    before = database.query("""
        SELECT
            cohort_month,
            months_since_first_purchase,
            customers,
            retained_customers,
            retention_rate
        FROM analytics.customer_cohorts
        ORDER BY
            cohort_month,
            months_since_first_purchase
    """)

    database.execute("""
        INSERT INTO raw.orders VALUES
            ('O7', 'C3', NULL)
    """)

    cohorts.build()

    after = database.query("""
        SELECT
            cohort_month,
            months_since_first_purchase,
            customers,
            retained_customers,
            retention_rate
        FROM analytics.customer_cohorts
        ORDER BY
            cohort_month,
            months_since_first_purchase
    """)

    assert after == before
