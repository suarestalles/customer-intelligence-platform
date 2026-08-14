from fastapi import HTTPException, status

from app.repositories.analytics_repo import AnalyticsRepository
from app.schemas.analytics_schema import (
    CategoryAnalyticsListResponse,
    CategoryAnalyticsResponse,
    CustomerCohortResponse,
    CustomerResponse,
    CustomerRFMResponse,
    CustomerSegmentResponse,
    CustomerSummaryResponse,
    KPIResponse,
    MonthlyRevenueResponse,
    ProductAnalyticsListResponse,
    ProductAnalyticsResponse,
    RevenueResponse,
)


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

    def get_customers(
        self,
        segment: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[CustomerResponse]:
        rows = self.repository.get_customers(segment, limit, offset)

        return [
            CustomerResponse(
                customer_id=row[0],
                total_orders=row[1],
                total_items=row[2],
                total_spent=float(row[3]),
                average_order_value=float(row[4]),
                first_order_date=row[5],
                last_order_date=row[6],
                customer_lifetime_days=row[7],
            )
            for row in rows
        ]

    def get_customer(self, customer_id: str) -> tuple[CustomerResponse, CustomerRFMResponse]:
        row = self.repository.get_customer(customer_id)

        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")
        customer = CustomerResponse(
            customer_id=row[0],
            total_orders=row[1],
            total_items=row[2],
            total_spent=float(row[3]),
            average_order_value=float(row[4]),
            first_order_date=row[5],
            last_order_date=row[6],
            customer_lifetime_days=row[7],
        )

        rfm = CustomerRFMResponse(
            customer_id=row[0],
            recency=row[8],
            frequency=row[9],
            monetary=float(row[10]),
            recency_score=row[11],
            frequency_score=row[12],
            monetary_score=row[13],
            rfm_score=row[14],
            segment=row[15],
        )

        return customer, rfm

    def get_kpis(self) -> KPIResponse:
        row = self.repository.get_kpis()

        return KPIResponse(
            total_customers=row[0],
            total_orders=row[1],
            total_revenue=float(row[2]),
            average_order_value=float(row[3]),
        )

    def get_revenue(self) -> RevenueResponse:
        total = self.repository.get_revenue()
        monthly = self.repository.get_monthly_revenue()

        return RevenueResponse(
            total_revenue=float(total[0]),
            total_orders=int(total[1]),
            average_order_value=float(total[2]),
            monthly=[
                MonthlyRevenueResponse(
                    month=row[0].date() if hasattr(row[0], "date") else row[0],
                    revenue=float(row[1]),
                    orders=int(row[2]),
                    average_order_value=float(row[3]),
                )
                for row in monthly
            ],
        )

    def get_products(
        self,
        category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> ProductAnalyticsListResponse:
        summary, rows = self.repository.get_products(
            category,
            limit,
            offset,
        )

        products = [
            ProductAnalyticsResponse(
                product_id=row[0],
                product_category=row[1],
                total_items=int(row[2]),
                total_orders=int(row[3]),
                total_revenue=float(row[4]),
                total_freight=float(row[5]),
                average_item_price=float(row[6]),
            )
            for row in rows
        ]

        return ProductAnalyticsListResponse(
            total_products=int(summary[0]),
            total_items=int(summary[1]),
            total_revenue=float(summary[2]),
            products=products,
        )

    def get_product_categories(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> CategoryAnalyticsListResponse:
        summary, rows = self.repository.get_product_categories(limit, offset)

        categories = [
            CategoryAnalyticsResponse(
                category=row[0],
                total_items=int(row[1]),
                total_orders=int(row[2]),
                total_revenue=float(row[3]),
                total_freight=float(row[4]),
            )
            for row in rows
        ]

        return CategoryAnalyticsListResponse(
            total_categories=int(summary[0]),
            categories=categories,
        )

    def get_customer_summary(self) -> CustomerSummaryResponse:
        row = self.repository.get_customer_summary()

        return CustomerSummaryResponse(
            total_customers=int(row[0]),
            total_revenue=float(row[1]),
            average_spend=float(row[2]),
            average_orders=float(row[3]),
        )

    def get_customer_cohorts(
        self,
    ) -> list[CustomerCohortResponse]:
        rows = self.repository.get_customer_cohorts()

        return [
            CustomerCohortResponse(
                cohort_month=row[0],
                months_since_first_purchase=row[1],
                customers=row[2],
                retained_customers=row[3],
                retention_rate=float(row[4]),
            )
            for row in rows
        ]
