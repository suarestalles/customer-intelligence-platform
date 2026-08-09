from pydantic import BaseModel


class CustomerSegmentResponse(BaseModel):
    segment: str
    customers: int
    average_spending: float
    average_frequency: float
    average_recency: float
