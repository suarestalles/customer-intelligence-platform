from pipelines.warehouse.database_config import Database


class CustomerFeatures:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_features AS

            SELECT
                cm.customer_unique_id,

                cm.total_orders,
                cm.total_items,
                cm.total_spent,
                cm.average_order_value,
                cm.first_order_date,
                cm.last_order_date,
                cm.customer_lifetime_days,

                rfm.recency,
                rfm.frequency,
                rfm.monetary,
                rfm.recency_score,
                rfm.frequency_score,
                rfm.monetary_score,
                rfm.rfm_score,
                rfm.segment

            FROM analytics.customer_metrics AS cm

            INNER JOIN analytics.customer_rfm AS rfm
                ON cm.customer_unique_id = rfm.customer_unique_id
        """

        self.database.execute(query)
