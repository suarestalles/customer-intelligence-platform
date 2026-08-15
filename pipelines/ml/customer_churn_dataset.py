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

            future_orders AS (
                SELECT DISTINCT
                    c.customer_unique_id
                FROM raw.orders AS o

                INNER JOIN raw.customers AS c
                    ON o.customer_id = c.customer_id

                CROSS JOIN cutoff_date

                WHERE o.order_purchase_timestamp IS NOT NULL

                    AND CAST(
                        o.order_purchase_timestamp AS DATE
                    ) > cutoff_date

                    AND CAST(
                        o.order_purchase_timestamp AS DATE
                    ) <= cutoff_date + INTERVAL '90 days'
            )

            SELECT
                cf.customer_unique_id,

                cf.total_orders,
                cf.total_items,
                cf.total_spent,
                cf.average_order_value,
                cf.first_order_date,
                cf.last_order_date,
                cf.customer_lifetime_days,
                cf.recency,
                cf.frequency,
                cf.monetary,

                CASE
                    WHEN fo.customer_unique_id IS NULL
                        THEN 1
                    ELSE 0
                END AS churn

            FROM analytics.customer_features AS cf

            LEFT JOIN future_orders AS fo
                ON cf.customer_unique_id =
                   fo.customer_unique_id
        """

        self.database.execute(query)
