from pipelines.warehouse.database_config import Database


class CustomerChurn:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_churn AS

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
                monetary,
                recency_score,
                frequency_score,
                monetary_score,
                rfm_score,
                segment,

                CASE
                    WHEN recency > 90 THEN 1
                    ELSE 0
                END AS churn

            FROM analytics.customer_features
        """

        self.database.execute(query)
