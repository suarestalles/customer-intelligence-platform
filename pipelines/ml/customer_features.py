from pipelines.warehouse.database_config import Database


class CustomerFeatures:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_features AS

            WITH reference_date AS (
                SELECT
                    MAX(
                        CAST(order_purchase_timestamp AS DATE)
                    ) AS max_order_date
                FROM raw.orders
                WHERE order_purchase_timestamp IS NOT NULL
            ),

            cutoff_date AS (
                SELECT
                    max_order_date - INTERVAL '90 days'
                    AS cutoff_date
                FROM reference_date
            ),

            customer_orders AS (
                SELECT
                    o.order_id,
                    c.customer_unique_id,
                    CAST(o.order_purchase_timestamp AS DATE)
                        AS order_date
                FROM raw.orders AS o

                INNER JOIN raw.customers AS c
                    ON o.customer_id = c.customer_id

                WHERE o.order_purchase_timestamp IS NOT NULL
            ),

            historical_orders AS (
                SELECT
                    co.order_id,
                    co.customer_unique_id,
                    co.order_date
                FROM customer_orders AS co

                CROSS JOIN cutoff_date

                WHERE co.order_date <= cutoff_date
            ),

            order_metrics AS (
                SELECT
                    ho.order_id,
                    ho.customer_unique_id,
                    ho.order_date,

                    COUNT(oi.order_item_id) AS total_items,

                    COALESCE(
                        SUM(oi.price),
                        0
                    ) AS order_value

                FROM historical_orders AS ho

                LEFT JOIN raw.order_items AS oi
                    ON ho.order_id = oi.order_id

                GROUP BY
                    ho.order_id,
                    ho.customer_unique_id,
                    ho.order_date
            ),

            customer_features AS (
                SELECT
                    customer_unique_id,

                    COUNT(DISTINCT order_id)
                        AS total_orders,

                    SUM(total_items)
                        AS total_items,

                    SUM(order_value)
                        AS total_spent,

                    AVG(order_value)
                        AS average_order_value,

                    MIN(order_date)
                        AS first_order_date,

                    MAX(order_date)
                        AS last_order_date,

                    DATE_DIFF(
                        'day',
                        MIN(order_date),
                        MAX(order_date)
                    ) AS customer_lifetime_days,

                    DATE_DIFF(
                        'day',
                        MAX(order_date),
                        cutoff_date
                    ) AS recency,

                    COUNT(DISTINCT order_id)
                        AS frequency,

                    SUM(order_value)
                        AS monetary

                FROM order_metrics

                CROSS JOIN cutoff_date

                GROUP BY
                    customer_unique_id,
                    cutoff_date
            )

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

            FROM customer_features
        """

        self.database.execute(query)
