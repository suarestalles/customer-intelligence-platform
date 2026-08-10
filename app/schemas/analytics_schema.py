from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class CustomerSegmentResponse(BaseModel):
    segment: str
    customers: int
    average_spending: float
    average_frequency: float
    average_recency: float


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    total_orders: int
    total_items: int
    total_spent: float
    average_order_value: float
    first_order_date: datetime | None
    last_order_date: datetime | None
    customer_lifetime_days: int | None


class CustomerRFMResponse(BaseModel):
    customer_id: str
    recency: int
    frequency: int
    monetary: float
    recency_score: int
    frequency_score: int
    monetary_score: int
    rfm_score: int
    segment: str


class KPIResponse(BaseModel):
    total_customers: int
    total_orders: int
    total_revenue: float
    average_order_value: float


class MonthlyRevenueResponse(BaseModel):
    month: date
    revenue: float
    orders: int
    average_order_value: float


class RevenueResponse(BaseModel):
    total_revenue: float
    total_orders: float
    average_order_value: float
    monthly: list[MonthlyRevenueResponse]
    order_status: str


class ProductAnalyticsResponse(BaseModel):
    product_id: str
    product_category: str | None
    total_items: int
    total_orders: int
    total_revenue: float
    total_freight: float
    average_item_price: float


class ProductAnalyticsListResponse(BaseModel):
    total_products: int
    total_items: int
    total_revenue: float
    products: list[ProductAnalyticsResponse]


class CategoryAnalyticsResponse(BaseModel):
    category: str | None
    total_items: int
    total_orders: int
    total_revenue: float
    total_freight: float


class CategoryAnalyticsListResponse(BaseModel):
    total_categories: int
    categories: list[CategoryAnalyticsResponse]
