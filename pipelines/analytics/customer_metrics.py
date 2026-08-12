from pipelines.warehouse.database_config import Database


class CustomerMetrics:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_metrics AS

            WITH delivered_orders AS (
                SELECT *
                FROM analytics.order_metrics AS om
                INNER JOIN raw.orders o
                    ON om.order_id = o.order_id
                WHERE o.order_status = 'delivered'
            )

            SELECT
                c.customer_unique_id,

                COUNT(DISTINCT o.order_id) AS total_orders,

                COALESCE(
                    SUM(o.total_items),
                    0
                ) AS total_items,

                COALESCE(
                    SUM(o.payment_value),
                    0
                ) AS total_spent,

                COALESCE(
                    SUM(o.payment_value)
                    / NULLIF(COUNT(DISTINCT o.order_id), 0),
                    0
                ) AS average_order_value,

                MIN(o.order_purchase_timestamp) AS first_order_date,

                MAX(o.order_purchase_timestamp) AS last_order_date,

                DATE_DIFF(
                    'day',
                    CAST(MIN(o.order_purchase_timestamp) AS DATE),
                    CAST(MAX(o.order_purchase_timestamp) AS DATE)
                ) AS customer_lifetime_days

            FROM raw.customers AS c

            LEFT JOIN delivered_orders AS o
                ON c.customer_id = o.customer_id

            GROUP BY
                c.customer_unique_id
        """

        self.database.execute(query)
