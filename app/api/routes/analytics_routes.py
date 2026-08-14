from fastapi import APIRouter, Depends, Query

from app.core.database import get_database
from app.repositories.analytics_repo import AnalyticsRepository
from app.schemas.analytics_schema import (
    CategoryAnalyticsListResponse,
    CustomerCohortResponse,
    CustomerResponse,
    CustomerRFMResponse,
    CustomerSegmentResponse,
    CustomerSummaryResponse,
    KPIResponse,
    ProductAnalyticsListResponse,
    RevenueResponse,
)
from app.services.analytics_service import AnalyticsService
from pipelines.warehouse.database_config import Database

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


def get_analytics_service(
    database: Database = Depends(get_database),
) -> AnalyticsService:
    repository = AnalyticsRepository(database)

    return AnalyticsService(repository)


@router.get("/segments", response_model=list[CustomerSegmentResponse])
def get_segment(
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[CustomerSegmentResponse]:
    return service.get_segments()


@router.get("/customers", response_model=list[CustomerResponse])
def get_customers(
    segment: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[CustomerResponse]:
    return service.get_customers(segment, limit, offset)


@router.get("/customer/{customer_id}")
def get_customer(
    customer_id: str, service: AnalyticsService = Depends(get_analytics_service)
) -> dict[str, CustomerResponse | CustomerRFMResponse]:
    customer, rfm = service.get_customer(customer_id)

    return {
        "customer": customer,
        "rfm": rfm,
    }


@router.get("/kpis", response_model=KPIResponse)
def get_kpis(service: AnalyticsService = Depends(get_analytics_service)) -> KPIResponse:
    return service.get_kpis()


@router.get("/revenue", response_model=RevenueResponse)
def get_revenue(service: AnalyticsService = Depends(get_analytics_service)) -> RevenueResponse:
    return service.get_revenue()


@router.get("/products", response_model=ProductAnalyticsListResponse)
def get_products(
    category: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: AnalyticsService = Depends(get_analytics_service),
) -> ProductAnalyticsListResponse:
    return service.get_products(category, limit, offset)


@router.get("/products/categories", response_model=CategoryAnalyticsListResponse)
def get_product_categories(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: AnalyticsService = Depends(get_analytics_service),
) -> CategoryAnalyticsListResponse:
    return service.get_product_categories(limit, offset)


@router.get("/customers/summary", response_model=CustomerSummaryResponse)
def get_customer_summary(
    service: AnalyticsService = Depends(get_analytics_service),
) -> CustomerSummaryResponse:
    return service.get_customer_summary()


@router.get("/cohorts", response_model=list[CustomerCohortResponse])
def get_customer_cohorts(
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[CustomerCohortResponse]:
    return service.get_customer_cohorts()
