from pipelines.warehouse.database_config import Database


class ChurnDataset:
    def __init__(
        self,
        database: Database,
        prediction_window_days: int = 90,
    ) -> None:
        self.database = database
        self.prediction_window_days = prediction_window_days

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = f"""
            CREATE OR REPLACE TABLE analytics.customer_churn_dataset AS

            WITH customer_orders AS (
                SELECT
                    c.customer_unique_id,
                    CAST(
                        o.order_purchase_timestamp AS DATE
                    ) AS order_date
                FROM raw.orders AS o
                INNER JOIN raw.customers AS c
                    ON o.customer_id = c.customer_id
                WHERE o.order_purchase_timestamp IS NOT NULL
            ),

            ranked_orders AS (
                SELECT
                    customer_unique_id,
                    order_date,

                    ROW_NUMBER() OVER (
                        PARTITION BY customer_unique_id
                        ORDER BY order_date
                    ) AS order_number,

                    COUNT(*) OVER (
                        PARTITION BY customer_unique_id
                    ) AS total_orders

                FROM customer_orders
            ),

            customer_features AS (
                SELECT
                    customer_unique_id,

                    CASE
                        WHEN total_orders >= 3
                            THEN total_orders - 1
                        ELSE total_orders
                    END AS total_orders,

                    MIN(order_date) AS first_order_date,

                    MAX(
                        CASE
                            WHEN order_number =
                                CASE
                                    WHEN total_orders >= 3
                                        THEN total_orders - 1
                                    ELSE total_orders
                                END
                            THEN order_date
                        END
                    ) AS last_order_date

                FROM ranked_orders

                WHERE total_orders >= 2

                GROUP BY
                    customer_unique_id,
                    total_orders
            ),

            customer_features_final AS (
                SELECT
                    customer_unique_id,
                    total_orders,
                    first_order_date,
                    last_order_date,

                    DATE_DIFF(
                        'day',
                        first_order_date,
                        last_order_date
                    ) AS customer_lifetime_days

                FROM customer_features
            ),

            dataset_dates AS (
                SELECT
                    MAX(order_date) AS max_order_date
                FROM customer_orders
            ),

            future_activity AS (
                SELECT DISTINCT
                    cf.customer_unique_id

                FROM customer_features_final AS cf

                INNER JOIN customer_orders AS co
                    ON co.customer_unique_id = cf.customer_unique_id

                WHERE
                    co.order_date > cf.last_order_date
                    AND co.order_date <=
                        cf.last_order_date
                        + INTERVAL '{self.prediction_window_days}' DAY
            )

            SELECT
                cf.customer_unique_id,

                cf.total_orders,
                cf.first_order_date,
                cf.last_order_date,
                cf.customer_lifetime_days,

                DATE_DIFF(
                    'day',
                    cf.last_order_date,
                    dd.max_order_date
                ) AS recency,

                CASE
                    WHEN fa.customer_unique_id IS NULL
                        THEN 1
                    ELSE 0
                END AS churn

            FROM customer_features_final AS cf

            CROSS JOIN dataset_dates AS dd

            LEFT JOIN future_activity AS fa
                ON cf.customer_unique_id = fa.customer_unique_id

            WHERE
                cf.last_order_date < dd.max_order_date
        """

        self.database.execute(query)
