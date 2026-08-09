from typing import Any

from pipelines.warehouse.database_config import Database


class AnalyticsRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_segments(self) -> list[tuple[Any, ...]]:
        query = """
            SELECT
                segment,
                COUNT(*) AS customers,
                AVG(monetary) AS average_spending,
                AVG(frequency) AS average_frequency,
                AVG(recency) AS average_recency
            FROM analytics.customer_rfm
            GROUP BY segment
            ORDER BY customers DESC
        """

        return self.database.query(query)
