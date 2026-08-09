from pipelines.warehouse.database_config import Database


class OrderMetrics:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
        CREATE OR REPLACE TABLE analytics.order_metrics AS
        
        WITH items AS(
            SELECT
                order_id,
                COUNT(*) AS total_items,
                SUM(price) AS product_value,
                SUM(freight_value) AS freight_value
            FROM raw.order_items
            GROUP BY order_id    
        ),

        payments AS (
            SELECT
                order_id,
                SUM(payment_value) AS payment_value
            FROM raw.order_payments
            GROUP BY order_id
        )

        SELECT
            o.order_id,
            o.customer_id,
            o.order_status,
            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_delivered_carrier_date,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,
            COALESCE(i.total_items, 0) AS total_items,
            COALESCE(i.product_value, 0) AS product_value,
            COALESCE(i.freight_value, 0) AS freight_value,
            COALESCE(p.payment_value, 0) AS payment_value
        FROM raw.orders AS o
        LEFT JOIN items AS i
            ON o.order_id = i.order_id
        LEFT JOIN payments AS p
            ON o.order_id = p.order_id
        """

        self.database.execute(query)
