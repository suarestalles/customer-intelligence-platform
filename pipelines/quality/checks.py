from dataclasses import dataclass, field
from typing import Any

from pipelines.quality.contracts import (
    ANALYTICS_COLUMN_TYPES,
    ANALYTICS_TABLE_CONTRACTS,
    RAW_COLUMN_TYPES,
    RAW_TABLE_CONTRACTS,
)
from pipelines.warehouse.database_config import Database


@dataclass(frozen=True, slots=True)
class QualityCheckResult:
    name: str
    passed: bool
    message: str
    details: dict[str, Any] = field(default_factory=dict)


def _result(
    name: str,
    passed: bool,
    message: str,
    **details: Any,
) -> QualityCheckResult:
    return QualityCheckResult(
        name=name,
        passed=passed,
        message=message,
        details=details,
    )


def table_exists(
    database: Database,
    schema: str,
    table: str,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = ?
          AND table_name = ?
        """,
        [schema, table],
    )

    exists = result[0][0] == 1

    return _result(
        name=f"table_exists:{schema}.{table}",
        passed=exists,
        message=(
            f"Table {schema}.{table} exists."
            if exists
            else f"Table {schema}.{table} does not exist."
        ),
    )


def table_not_empty(
    database: Database,
    schema: str,
    table: str,
) -> QualityCheckResult:
    result = database.query(
        f"""
        SELECT COUNT(*)
        FROM {schema}.{table}
        """
    )

    row_count = result[0][0]
    passed = row_count > 0

    return _result(
        name=f"table_not_empty:{schema}.{table}",
        passed=passed,
        message=(
            f"Table {schema}.{table} contains {row_count} rows."
            if passed
            else f"Table {schema}.{table} is empty."
        ),
        row_count=row_count,
    )


def no_nulls(
    database: Database,
    schema: str,
    table: str,
    column: str,
) -> QualityCheckResult:
    result = database.query(
        f"""
        SELECT COUNT(*)
        FROM {schema}.{table}
        WHERE {column} IS NULL
        """
    )

    null_count = result[0][0]
    passed = null_count == 0

    return _result(
        name=f"no_nulls:{schema}.{table}.{column}",
        passed=passed,
        message=(
            f"Column {schema}.{table}.{column} contains no null values."
            if passed
            else (f"Column {schema}.{table}.{column} contains {null_count} null values.")
        ),
        null_count=null_count,
    )


def unique_column(
    database: Database,
    schema: str,
    table: str,
    column: str,
) -> QualityCheckResult:
    result = database.query(
        f"""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT {column}) AS distinct_values
        FROM {schema}.{table}
        """
    )

    total_rows, distinct_values = result[0]

    passed = total_rows == distinct_values

    return _result(
        name=f"unique:{schema}.{table}.{column}",
        passed=passed,
        message=(
            f"Column {schema}.{table}.{column} is unique."
            if passed
            else (f"Column {schema}.{table}.{column} contains duplicate values.")
        ),
        total_rows=total_rows,
        distinct_values=distinct_values,
    )


def unique_combination(
    database: Database,
    schema: str,
    table: str,
    columns: tuple[str, ...],
) -> QualityCheckResult:
    column_list = ", ".join(columns)

    result = database.query(
        f"""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT ({column_list})) AS distinct_values
        FROM {schema}.{table}
        """
    )

    total_rows, distinct_values = result[0]
    passed = total_rows == distinct_values

    return _result(
        name=(f"unique:{schema}.{table}.{','.join(columns)}"),
        passed=passed,
        message=(
            f"Combination ({column_list}) is unique."
            if passed
            else f"Combination ({column_list}) contains duplicates."
        ),
        total_rows=total_rows,
        distinct_values=distinct_values,
    )


def non_negative(
    database: Database,
    schema: str,
    table: str,
    column: str,
) -> QualityCheckResult:
    result = database.query(
        f"""
        SELECT COUNT(*)
        FROM {schema}.{table}
        WHERE {column} < 0
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name=f"non_negative:{schema}.{table}.{column}",
        passed=passed,
        message=(
            f"Column {schema}.{table}.{column} contains no negative values."
            if passed
            else (f"Column {schema}.{table}.{column} contains {invalid_count} negative values.")
        ),
        invalid_count=invalid_count,
    )


def non_negative_or_zero_null(
    database: Database,
    schema: str,
    table: str,
    column: str,
) -> QualityCheckResult:
    result = database.query(
        f"""
        SELECT COUNT(*)
        FROM {schema}.{table}
        WHERE {column} IS NOT NULL
          AND {column} < 0
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name=f"non_negative:{schema}.{table}.{column}",
        passed=passed,
        message=(
            f"Column {schema}.{table}.{column} contains no negative values."
            if passed
            else (f"Column {schema}.{table}.{column} contains {invalid_count} negative values.")
        ),
        invalid_count=invalid_count,
    )


def foreign_key_integrity(
    database: Database,
    child_schema: str,
    child_table: str,
    child_column: str,
    parent_schema: str,
    parent_table: str,
    parent_column: str,
) -> QualityCheckResult:
    result = database.query(
        f"""
        SELECT COUNT(*)
        FROM {child_schema}.{child_table} AS child
        LEFT JOIN {parent_schema}.{parent_table} AS parent
            ON child.{child_column} = parent.{parent_column}
        WHERE child.{child_column} IS NOT NULL
          AND parent.{parent_column} IS NULL
        """
    )

    orphan_count = result[0][0]
    passed = orphan_count == 0

    return _result(
        name=(
            f"foreign_key:{child_schema}.{child_table}."
            f"{child_column}->{parent_schema}.{parent_table}."
            f"{parent_column}"
        ),
        passed=passed,
        message=(
            "Foreign-key integrity is valid." if passed else f"Found {orphan_count} orphan records."
        ),
        orphan_count=orphan_count,
    )


def columns_exist(
    database: Database,
    schema: str,
    table: str,
    columns: tuple[str, ...],
) -> QualityCheckResult:
    placeholders = ", ".join("?" for _ in columns)

    result = database.query(
        f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = ?
          AND table_name = ?
          AND column_name IN ({placeholders})
        """,
        [schema, table, *columns],
    )

    found = {row[0] for row in result}
    expected = set(columns)
    missing = sorted(expected - found)

    passed = not missing

    return _result(
        name=f"columns_exist:{schema}.{table}",
        passed=passed,
        message=(
            f"All required columns exist in {schema}.{table}."
            if passed
            else (f"Missing columns in {schema}.{table}: {', '.join(missing)}.")
        ),
        missing_columns=missing,
    )


def order_metrics_match_raw_orders(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT
            (SELECT COUNT(*) FROM raw.orders) AS raw_orders,
            (SELECT COUNT(*) FROM analytics.order_metrics) AS metric_orders,
            (
                SELECT COUNT(DISTINCT order_id)
                FROM analytics.order_metrics
            ) AS unique_metric_orders
        """
    )

    raw_orders, metric_orders, unique_metric_orders = result[0]

    passed = raw_orders == metric_orders and metric_orders == unique_metric_orders

    return _result(
        name="analytics.order_metrics_matches_raw_orders",
        passed=passed,
        message=(
            "analytics.order_metrics contains exactly one row for every raw order."
            if passed
            else ("analytics.order_metrics does not match raw.orders.")
        ),
        raw_orders=raw_orders,
        metric_orders=metric_orders,
        unique_metric_orders=unique_metric_orders,
    )


def order_metrics_revenue_matches_raw_payments(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT
            (
                SELECT COALESCE(SUM(payment_value), 0)
                FROM raw.order_payments
            ) AS raw_revenue,
            (
                SELECT COALESCE(SUM(payment_value), 0)
                FROM analytics.order_metrics
            ) AS metric_revenue
        """
    )

    raw_revenue, metric_revenue = result[0]

    difference = abs(float(raw_revenue) - float(metric_revenue))
    tolerance = 0.01

    passed = difference <= tolerance

    return _result(
        name="analytics.order_metrics_revenue_matches_raw_payments",
        passed=passed,
        message=(
            f"Analytics revenue matches raw payment revenue within tolerance of R$ {tolerance:.2f}."
            if passed
            else (
                "Analytics revenue does not match raw payment revenue. "
                f"Difference: R$ {difference:.2f}."
            )
        ),
        raw_revenue=raw_revenue,
        metric_revenue=metric_revenue,
        difference=difference,
        tolerance=tolerance,
    )


def customer_metrics_unique(
    database: Database,
) -> QualityCheckResult:
    return unique_column(
        database,
        "analytics",
        "customer_metrics",
        "customer_unique_id",
    )


def customer_metrics_dates_valid(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT COUNT(*)
        FROM analytics.customer_metrics
        WHERE first_order_date IS NOT NULL
          AND last_order_date IS NOT NULL
          AND first_order_date > last_order_date
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name="analytics.customer_metrics_dates_valid",
        passed=passed,
        message=(
            "Customer order dates are consistent."
            if passed
            else (
                f"Found {invalid_count} customers where first_order_date is after last_order_date."
            )
        ),
        invalid_count=invalid_count,
    )


def customer_metrics_lifetime_valid(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT COUNT(*)
        FROM analytics.customer_metrics
        WHERE customer_lifetime_days < 0
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name="analytics.customer_metrics_lifetime_valid",
        passed=passed,
        message=(
            "Customer lifetime values are valid."
            if passed
            else (f"Found {invalid_count} customers with negative lifetime days.")
        ),
        invalid_count=invalid_count,
    )


def customer_metrics_values_valid(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT COUNT(*)
        FROM analytics.customer_metrics
        WHERE total_orders < 0
           OR total_items < 0
           OR total_spent < 0
           OR average_order_value < 0
           OR customer_lifetime_days < 0
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name="analytics.customer_metrics_values_valid",
        passed=passed,
        message=(
            "Customer metric values are valid."
            if passed
            else (f"Found {invalid_count} customers with invalid metric values.")
        ),
        invalid_count=invalid_count,
    )


def rfm_scores_valid(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT COUNT(*)
        FROM analytics.customer_rfm
        WHERE recency < 0
           OR frequency <= 0
           OR monetary < 0
           OR recency_score NOT BETWEEN 1 AND 5
           OR frequency_score NOT BETWEEN 1 AND 5
           OR monetary_score NOT BETWEEN 1 AND 5
           OR rfm_score NOT BETWEEN 3 AND 15
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name="analytics.customer_rfm_scores_valid",
        passed=passed,
        message=(
            "RFM scores and metrics are valid."
            if passed
            else (f"Found {invalid_count} invalid RFM records.")
        ),
        invalid_count=invalid_count,
    )


def rfm_score_consistent(
    database: Database,
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT COUNT(*)
        FROM analytics.customer_rfm
        WHERE rfm_score != (
            recency_score
            + frequency_score
            + monetary_score
        )
        """
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name="analytics.customer_rfm_score_consistent",
        passed=passed,
        message=(
            "RFM score equals the sum of its component scores."
            if passed
            else (f"Found {invalid_count} records with inconsistent RFM scores.")
        ),
        invalid_count=invalid_count,
    )


def rfm_segments_valid(
    database: Database,
) -> QualityCheckResult:
    valid_segments = (
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "At Risk",
        "Lost",
    )

    placeholders = ", ".join("?" for _ in valid_segments)

    result = database.query(
        f"""
        SELECT
            COUNT(*)
        FROM analytics.customer_rfm
        WHERE segment NOT IN ({placeholders})
           OR segment IS NULL
        """,
        list(valid_segments),
    )

    invalid_count = result[0][0]
    passed = invalid_count == 0

    return _result(
        name="analytics.customer_rfm_segments_valid",
        passed=passed,
        message=(
            "All RFM segments are valid."
            if passed
            else (f"Found {invalid_count} records with invalid RFM segments.")
        ),
        invalid_count=invalid_count,
    )


def rfm_customer_ids_unique(
    database: Database,
) -> QualityCheckResult:
    return unique_column(
        database,
        "analytics",
        "customer_rfm",
        "customer_unique_id",
    )


def raw_quality_checks(
    database: Database,
) -> list[QualityCheckResult]:
    results: list[QualityCheckResult] = []

    required_tables = (
        "customers",
        "orders",
        "order_items",
        "order_payments",
        "products",
    )

    for table in required_tables:
        result = table_exists(database, "raw", table)
        results.append(result)

        if result.passed:
            results.append(table_not_empty(database, "raw", table))

    for table, columns in RAW_TABLE_CONTRACTS.items():
        if table_exists(database, "raw", table).passed:
            results.append(
                columns_exist(
                    database,
                    "raw",
                    table,
                    columns,
                )
            )

    for table, column_types in RAW_COLUMN_TYPES.items():
        if table_exists(database, "raw", table).passed:
            results.append(
                column_types_match(
                    database,
                    "raw",
                    table,
                    column_types,
                )
            )

    column_checks = (
        ("customers", "customer_id"),
        ("customers", "customer_unique_id"),
        ("orders", "order_id"),
        ("orders", "customer_id"),
        ("orders", "order_purchase_timestamp"),
        ("order_items", "order_id"),
        ("order_payments", "order_id"),
        ("order_payments", "payment_value"),
        ("products", "product_id"),
    )

    for table, column in column_checks:
        if table_exists(database, "raw", table).passed:
            results.append(no_nulls(database, "raw", table, column))

    if table_exists(database, "raw", "customers").passed:
        results.append(
            unique_column(
                database,
                "raw",
                "customers",
                "customer_id",
            )
        )

    if table_exists(database, "raw", "orders").passed:
        results.append(
            unique_column(
                database,
                "raw",
                "orders",
                "order_id",
            )
        )

    if table_exists(database, "raw", "products").passed:
        results.append(
            unique_column(
                database,
                "raw",
                "products",
                "product_id",
            )
        )

    if table_exists(database, "raw", "order_items").passed:
        results.append(
            unique_combination(
                database,
                "raw",
                "order_items",
                ("order_id", "order_item_id"),
            )
        )

    if table_exists(database, "raw", "orders").passed:
        results.append(
            foreign_key_integrity(
                database,
                "raw",
                "orders",
                "customer_id",
                "raw",
                "customers",
                "customer_id",
            )
        )

    if table_exists(database, "raw", "order_items").passed:
        results.append(
            foreign_key_integrity(
                database,
                "raw",
                "order_items",
                "order_id",
                "raw",
                "orders",
                "order_id",
            )
        )

    if table_exists(database, "raw", "order_payments").passed:
        results.append(
            foreign_key_integrity(
                database,
                "raw",
                "order_payments",
                "order_id",
                "raw",
                "orders",
                "order_id",
            )
        )

        results.append(
            non_negative(
                database,
                "raw",
                "order_payments",
                "payment_value",
            )
        )

    if table_exists(database, "raw", "order_items").passed:
        results.extend(
            [
                non_negative(
                    database,
                    "raw",
                    "order_items",
                    "price",
                ),
                non_negative(
                    database,
                    "raw",
                    "order_items",
                    "freight_value",
                ),
            ]
        )

    return results


def analytics_quality_checks(
    database: Database,
) -> list[QualityCheckResult]:
    results: list[QualityCheckResult] = []

    required_tables = (
        "order_metrics",
        "customer_metrics",
        "customer_rfm",
    )

    for table in required_tables:
        result = table_exists(database, "analytics", table)
        results.append(result)

        if result.passed:
            results.append(table_not_empty(database, "analytics", table))

    for table, columns in ANALYTICS_TABLE_CONTRACTS.items():
        if table_exists(database, "analytics", table).passed:
            results.append(
                columns_exist(
                    database,
                    "analytics",
                    table,
                    columns,
                )
            )

    for table, column_types in ANALYTICS_COLUMN_TYPES.items():
        if table_exists(database, "analytics", table).passed:
            results.append(
                column_types_match(
                    database,
                    "analytics",
                    table,
                    column_types,
                )
            )

    if table_exists(database, "analytics", "order_metrics").passed:
        results.extend(
            [
                unique_column(
                    database,
                    "analytics",
                    "order_metrics",
                    "order_id",
                ),
                order_metrics_match_raw_orders(database),
                order_metrics_revenue_matches_raw_payments(database),
                non_negative(
                    database,
                    "analytics",
                    "order_metrics",
                    "total_items",
                ),
                non_negative(
                    database,
                    "analytics",
                    "order_metrics",
                    "product_value",
                ),
                non_negative(
                    database,
                    "analytics",
                    "order_metrics",
                    "freight_value",
                ),
                non_negative(
                    database,
                    "analytics",
                    "order_metrics",
                    "payment_value",
                ),
            ]
        )

    if table_exists(database, "analytics", "customer_metrics").passed:
        results.extend(
            [
                customer_metrics_unique(database),
                customer_metrics_values_valid(database),
                customer_metrics_dates_valid(database),
                customer_metrics_lifetime_valid(database),
            ]
        )

    if table_exists(database, "analytics", "customer_rfm").passed:
        results.extend(
            [
                rfm_customer_ids_unique(database),
                rfm_scores_valid(database),
                rfm_score_consistent(database),
                rfm_segments_valid(database),
            ]
        )

    return results


def column_types_match(
    database: Database,
    schema: str,
    table: str,
    expected_types: dict[str, str],
) -> QualityCheckResult:
    result = database.query(
        """
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = ?
          AND table_name = ?
        """,
        [schema, table],
    )

    actual_types = {row[0]: row[1] for row in result}

    mismatches: dict[str, dict[str, str | None]] = {}

    for column, expected_type in expected_types.items():
        actual_type = actual_types.get(column)

        if actual_type != expected_type:
            mismatches[column] = {
                "expected": expected_type,
                "actual": actual_type,
            }

    passed = not mismatches

    return _result(
        name=f"column_types:{schema}.{table}",
        passed=passed,
        message=(
            f"All column types match the contract for {schema}.{table}."
            if passed
            else (f"Found {len(mismatches)} column type mismatches in {schema}.{table}.")
        ),
        mismatches=mismatches,
    )
