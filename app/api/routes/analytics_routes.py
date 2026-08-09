from fastapi import APIRouter, Depends

from app.core.database import get_database
from app.schemas.analytics_schema import CustomerSegmentResponse
from app.services.analytics_service import AnalyticsService
from pipelines.warehouse.database_config import Database

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


def get_analytics_service(
    database: Database = Depends(get_database),
) -> AnalyticsService:
    from app.repositories.analytics_repo import AnalyticsRepository

    repository = AnalyticsRepository(database)

    return AnalyticsService(repository)


@router.get("/segments", response_model=list[CustomerSegmentResponse])
def get_segment(
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[CustomerSegmentResponse]:
    return service.get_segments()
