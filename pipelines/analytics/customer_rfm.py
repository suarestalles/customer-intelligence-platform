from pipelines.warehouse.database_config import Database


class CustomerRFM:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build(self) -> None:
        self.database.create_schema("analytics")

        query = """
            CREATE OR REPLACE TABLE analytics.customer_rfm AS
            
            WITH reference_date AS (
                SELECT
                    MAX(last_order_date) AS max_order_date
                FROM analytics.customer_metrics
            ),

            rfm AS (
                SELECT
                    customer_unique_id,
                    DATE_DIFF(
                        'day',
                        CAST(last_order_date AS DATE),
                        CAST(
                            max_order_date AS DATE
                        )
                    ) AS recency,

                    total_orders AS frequency,
                    total_spent AS monetary
                FROM analytics.customer_metrics
                CROSS JOIN reference_date
                WHERE total_orders > 0
            ),

            scores AS (
                SELECT
                    customer_unique_id,
                    recency,
                    frequency,
                    monetary,

                    NTILE(5) OVER (
                        ORDER BY recency ASC
                    ) AS recency_score,
                    
                    NTILE(5) OVER (
                        ORDER BY frequency DESC
                    ) AS frequency_score,
                    
                    NTILE(5) OVER (
                        ORDER BY monetary DESC
                    ) AS monetary_score
                FROM rfm
            )

            SELECT
                *,
                recency_score
                + frequency_score
                + monetary_score AS rfm_score,

                CASE
                    WHEN (
                        recency_score
                        + frequency_score
                        + monetary_score
                    ) >= 13
                        THEN 'Champions'
                    WHEN (
                        recency_score
                        + frequency_score
                        + monetary_score
                    ) >= 10
                        THEN 'Loyal Customers'
                    WHEN (
                        recency_score
                        + frequency_score
                        + monetary_score
                    ) >= 7
                        THEN 'Potential Loyalists'
                    WHEN (
                        recency_score
                        + frequency_score
                        + monetary_score
                    ) >= 4
                        THEN 'At Risk'
                    ELSE 'Lost'
                END AS segment
            FROM scores
        """

        self.database.execute(query)
