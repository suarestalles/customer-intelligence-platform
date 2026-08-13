from unittest.mock import MagicMock

from pipelines.quality.checks import column_types_match, columns_exist


def test_columns_exist_passes_when_all_columns_are_present() -> None:
    database = MagicMock()

    database.query.return_value = [
        ("order_id",),
        ("customer_id",),
        ("order_status",),
    ]

    result = columns_exist(
        database,
        "raw",
        "orders",
        (
            "order_id",
            "customer_id",
            "order_status",
        ),
    )

    assert result.passed is True
    assert result.name == "columns_exist:raw.orders"
    assert result.details["missing_columns"] == []


def test_columns_exist_fails_when_column_is_missing() -> None:
    database = MagicMock()

    database.query.return_value = [
        ("order_id",),
        ("order_status",),
    ]

    result = columns_exist(
        database,
        "raw",
        "orders",
        (
            "order_id",
            "customer_id",
            "order_status",
        ),
    )

    assert result.passed is False
    assert result.name == "columns_exist:raw.orders"
    assert result.details["missing_columns"] == ["customer_id"]


def test_columns_exist_passes_when_extra_columns_exist() -> None:
    database = MagicMock()

    database.query.return_value = [
        ("order_id",),
        ("customer_id",),
        ("order_status",),
        ("new_column",),
    ]

    result = columns_exist(
        database,
        "raw",
        "orders",
        (
            "order_id",
            "customer_id",
            "order_status",
        ),
    )

    assert result.passed is True
    assert result.details["missing_columns"] == []


def test_columns_exist_fails_when_no_columns_are_found() -> None:
    database = MagicMock()
    database.query.return_value = []

    result = columns_exist(
        database,
        "raw",
        "orders",
        (
            "order_id",
            "customer_id",
        ),
    )

    assert result.passed is False
    assert result.details["missing_columns"] == [
        "customer_id",
        "order_id",
    ]


def test_column_types_match_passes_when_types_are_correct() -> None:
    database = MagicMock()

    database.query.return_value = [
        ("order_id", "VARCHAR"),
        ("customer_id", "VARCHAR"),
        ("order_purchase_timestamp", "TIMESTAMP"),
    ]

    result = column_types_match(
        database,
        "raw",
        "orders",
        {
            "order_id": "VARCHAR",
            "customer_id": "VARCHAR",
            "order_purchase_timestamp": "TIMESTAMP",
        },
    )

    assert result.passed is True
    assert result.name == "column_types:raw.orders"
    assert result.details["mismatches"] == {}


def test_column_types_match_fails_when_type_is_incorrect() -> None:
    database = MagicMock()

    database.query.return_value = [
        ("order_id", "VARCHAR"),
        ("customer_id", "VARCHAR"),
        ("order_purchase_timestamp", "VARCHAR"),
    ]

    result = column_types_match(
        database,
        "raw",
        "orders",
        {
            "order_id": "VARCHAR",
            "customer_id": "VARCHAR",
            "order_purchase_timestamp": "TIMESTAMP",
        },
    )

    assert result.passed is False

    assert result.details["mismatches"] == {
        "order_purchase_timestamp": {
            "expected": "TIMESTAMP",
            "actual": "VARCHAR",
        }
    }


def test_column_types_match_fails_when_column_is_missing() -> None:
    database = MagicMock()

    database.query.return_value = [
        ("order_id", "VARCHAR"),
    ]

    result = column_types_match(
        database,
        "raw",
        "orders",
        {
            "order_id": "VARCHAR",
            "customer_id": "VARCHAR",
        },
    )

    assert result.passed is False

    assert result.details["mismatches"] == {
        "customer_id": {
            "expected": "VARCHAR",
            "actual": None,
        }
    }
