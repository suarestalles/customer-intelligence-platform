from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "data" / "warehouse" / "customer_intelligence.duckdb"


def main() -> None:
    connection = duckdb.connect(str(DATABASE_PATH))

    # tables = connection.execute(
    #     """
    #         SELECT
    #             table_schema,
    #             table_name
    #         FROM information_schema.tables
    #         WHERE table_schema = 'raw'
    #         ORDER BY table_name
    #     """
    # ).fetchall()

    # print("Raw Tables:")
    # for schema, table in tables:
    #     print(f"- {schema}.{table}")

    # count = connection.execute("SELECT COUNT(*) FROM raw.customers").fetchone()

    # print(f"\nCustomers: {count[0]}")

    # result = connection.execute(
    #     """
    #         SELECT
    #             order_id,
    #             COUNT(*) AS payment_rows
    #         FROM raw.order_payments
    #         GROUP BY order_id
    #         HAVING COUNT(*) > 1
    #         ORDER BY payment_rows DESC
    #         LIMIT 10;
    #     """
    # ).fetchall()

    # result2 = connection.execute(
    #     """
    #         SELECT
    #             order_id,
    #             COUNT(*) AS item_rows
    #         FROM raw.order_items
    #         GROUP BY order_id
    #         HAVING COUNT(*) > 1
    #         ORDER BY item_rows DESC
    #         LIMIT 10;
    #     """
    # ).fetchall()

    # for r in result:
    #     print(f"############################ RESULT: {r}")

    # for r2 in result2:
    #     print(f"############################ RESULT 2: {r2}")

    # result = connection.execute(
    #     """
    #         SELECT * FROM analytics.order_metrics LIMIT 10
    #     """
    # ).fetchall()

    # result2 = connection.execute(
    #     """
    #         SELECT
    #             COUNT(*) AS total_orders,
    #             COUNT(DISTINCT order_id) AS unique_orders
    #         FROM analytics.order_metrics
    #     """
    # ).fetchall()

    # print(f"RESULT 1 -> {result}")
    # print(f"RESULT 2 -> {result2}")

    # result = connection.execute(
    #     """
    #         SELECT SUM(payment_value) AS total_revenue FROM analytics.order_metrics
    #     """
    # ).fetchall()

    # result2 = connection.execute(
    #     """
    #         SELECT
    #             SUM(payment_value) AS total_revenue FROM raw.order_payments
    #     """
    # ).fetchall()

    # print(f"RESULT 1 -> {result}")
    # print(f"RESULT 2 -> {result2}")

    # result = connection.execute(
    #     """
    #     SELECT
    #         COUNT(*) AS customers_without_orders
    #     FROM analytics.customer_metrics
    #     WHERE total_orders = 0;
    #     """
    # ).fetchone()

    # print(f"RESULT 1 -> {result}")

    result = connection.execute(
        """
        SELECT
            customer_unique_id,
            recency,
            frequency,
            monetary,
            rfm_score,
            segment
        FROM analytics.customer_rfm
        ORDER BY rfm_score DESC
        LIMIT 20;
        """
    ).fetchall()

    print(f"RESULT 1 -> {result}")

    connection.close()


if __name__ == "__main__":
    main()
