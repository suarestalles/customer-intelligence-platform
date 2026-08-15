from pipelines.warehouse.database_config import Database


class CustomerChurnDataset:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_churn_dataset AS

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
                    customer_unique_id,
                    order_date
                FROM customer_orders
                CROSS JOIN cutoff_date
                WHERE order_date <= cutoff_date
            ),

            customer_features AS (
                SELECT
                    customer_unique_id,

                    COUNT(*) AS frequency,

                    MIN(order_date) AS first_order_date,

                    MAX(order_date) AS last_order_date,

                    DATE_DIFF(
                        'day',
                        MIN(order_date),
                        MAX(order_date)
                    ) AS customer_lifetime_days,

                    DATE_DIFF(
                        'day',
                        MAX(order_date),
                        cutoff_date
                    ) AS recency

                FROM historical_orders

                CROSS JOIN cutoff_date

                GROUP BY
                    customer_unique_id,
                    cutoff_date
            ),

            future_orders AS (
                SELECT DISTINCT
                    ho.customer_unique_id
                FROM customer_orders AS ho

                CROSS JOIN cutoff_date

                WHERE ho.order_date > cutoff_date
                    AND ho.order_date <= cutoff_date + INTERVAL '90 days'
            )

            SELECT
                cf.customer_unique_id,

                cf.frequency,
                cf.first_order_date,
                cf.last_order_date,
                cf.customer_lifetime_days,
                cf.recency,

                CASE
                    WHEN fo.customer_unique_id IS NULL
                        THEN 1
                    ELSE 0
                END AS churn

            FROM customer_features AS cf

            LEFT JOIN future_orders AS fo
                ON cf.customer_unique_id =
                   fo.customer_unique_id
        """

        self.database.execute(query)
