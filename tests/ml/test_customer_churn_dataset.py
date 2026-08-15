from decimal import Decimal
from pathlib import Path

from pipelines.ml.customer_churn_dataset import CustomerChurnDataset
from pipelines.ml.customer_features import CustomerFeatures
from tests.ml.test_customer_features import create_test_database


def test_customer_churn_dataset_should_create_churn_label(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()
    CustomerChurnDataset(database).build()

    result = database.query(
        """
        SELECT
            customer_unique_id,
            churn
        FROM analytics.customer_churn_dataset
        ORDER BY customer_unique_id
        """
    )

    assert result == [
        ("unique-1", 0),
        ("unique-2", 0),
        ("unique-3", 1),
    ]


def test_customer_churn_dataset_should_have_valid_labels(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()
    CustomerChurnDataset(database).build()

    invalid_labels = database.query(
        """
        SELECT churn
        FROM analytics.customer_churn_dataset
        WHERE churn NOT IN (0, 1)
        """
    )

    assert invalid_labels == []


def test_customer_churn_dataset_should_have_unique_customers(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()
    CustomerChurnDataset(database).build()

    duplicates = database.query(
        """
        SELECT
            customer_unique_id,
            COUNT(*) AS row_count
        FROM analytics.customer_churn_dataset
        GROUP BY customer_unique_id
        HAVING COUNT(*) > 1
        """
    )

    assert duplicates == []


def test_customer_churn_dataset_should_contain_model_features(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()
    CustomerChurnDataset(database).build()

    columns = database.query(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'analytics'
          AND table_name = 'customer_churn_dataset'
        ORDER BY ordinal_position
        """
    )

    column_names = [row[0] for row in columns]

    expected_columns = [
        "customer_unique_id",
        "total_orders",
        "total_items",
        "total_spent",
        "average_order_value",
        "first_order_date",
        "last_order_date",
        "customer_lifetime_days",
        "recency",
        "frequency",
        "monetary",
        "churn",
    ]

    assert column_names == expected_columns


def test_customer_churn_dataset_should_use_customer_features(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = create_test_database(database_path)

    CustomerFeatures(database).build()
    CustomerChurnDataset(database).build()

    result = database.query(
        """
        SELECT
            customer_unique_id,
            total_orders,
            total_items,
            total_spent,
            frequency,
            monetary,
            churn
        FROM analytics.customer_churn_dataset
        ORDER BY customer_unique_id
        """
    )

    assert result == [
        (
            "unique-1",
            2,
            3,
            Decimal("350.00"),
            2,
            Decimal("350.00"),
            0,
        ),
        (
            "unique-2",
            1,
            1,
            Decimal("80.00"),
            1,
            Decimal("80.00"),
            0,
        ),
        (
            "unique-3",
            1,
            1,
            Decimal("120.00"),
            1,
            Decimal("120.00"),
            1,
        ),
    ]
