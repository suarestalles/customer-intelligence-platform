from pipelines.warehouse.database_config import Database


class CustomerCohorts:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_cohorts AS

            WITH customer_orders AS (
                SELECT
                    c.customer_unique_id,
                    CAST(
                        DATE_TRUNC(
                            'month',
                            CAST(o.order_purchase_timestamp AS DATE)
                        ) AS DATE
                    ) AS order_month
                FROM raw.orders AS o
                INNER JOIN raw.customers AS c
                    ON o.customer_id = c.customer_id
                WHERE o.order_purchase_timestamp IS NOT NULL
            ),

            customer_first_purchase AS (
                SELECT
                    customer_unique_id,
                    MIN(order_month) AS cohort_month
                FROM customer_orders
                GROUP BY customer_unique_id
            ),

            customer_activity AS (
                SELECT DISTINCT
                    co.customer_unique_id,
                    fp.cohort_month,
                    co.order_month
                FROM customer_orders AS co
                INNER JOIN customer_first_purchase AS fp
                    ON co.customer_unique_id = fp.customer_unique_id
            ),

            cohort_activity AS (
                SELECT
                    cohort_month,
                    DATE_DIFF(
                        'month',
                        cohort_month,
                        order_month
                    ) AS months_since_first_purchase,
                    COUNT(DISTINCT customer_unique_id) AS retained_customers
                FROM customer_activity
                GROUP BY
                    cohort_month,
                    months_since_first_purchase
            ),

            cohort_sizes AS (
                SELECT
                    cohort_month,
                    MAX(retained_customers) AS cohort_size
                FROM cohort_activity
                WHERE months_since_first_purchase = 0
                GROUP BY cohort_month
            )

            SELECT
                ca.cohort_month,
                ca.months_since_first_purchase,
                cs.cohort_size AS customers,
                ca.retained_customers,
                ROUND(
                    100.0
                    * ca.retained_customers
                    / NULLIF(cs.cohort_size, 0),
                    2
                ) AS retention_rate
            FROM cohort_activity AS ca
            INNER JOIN cohort_sizes AS cs
                ON ca.cohort_month = cs.cohort_month
            ORDER BY
                ca.cohort_month,
                ca.months_since_first_purchase
        """

        self.database.execute(query)
