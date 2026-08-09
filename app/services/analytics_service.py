from app.repositories.analytics_repo import AnalyticsRepository
from app.schemas.analytics_schema import CustomerSegmentResponse


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    def get_segments(self) -> list[CustomerSegmentResponse]:
        rows = self.repository.get_segments()

        return [
            CustomerSegmentResponse(
                segment=row[0],
                customers=row[1],
                average_spending=float(row[2]),
                average_frequency=float(row[3]),
                average_recency=float(row[4]),
            )
            for row in rows
        ]
