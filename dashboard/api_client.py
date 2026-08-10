from typing import Any

import httpx2


class AnalyticsAPIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def _get(self, endpoint: str) -> Any:
        response = httpx2.get(f"{self.base_url}{endpoint}", timeout=10.0)

        response.raise_for_status()

        return response.json()

    def get_kpis(self) -> dict[str, Any]:
        return self._get("/api/v1/analytics/kpis")

    def get_revenue(self) -> dict[str, Any]:
        return self._get("/api/v1/analytics/revenue")

    def get_segments(self) -> dict[str, Any]:
        return self._get("/api/v1/analytics/segments")

    def get_customers(
        self,
        segment: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        endpoint = f"/api/v1/analytics/customers?limit={limit}&offset={offset}"

        if segment:
            endpoint += f"&segment={segment}"

        return self._get(endpoint)

    def get_products(
        self, category: str | None = None, limit: int = 20, offset: int = 0
    ) -> dict[str, Any]:
        endpoint = f"/api/v1/analytics/products?limit={limit}&offset={offset}"

        if category:
            endpoint += f"&category={category}"

        return self._get(endpoint)

    def get_product_categories(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        return self._get(f"/api/v1/analytics/products/categories?limit={limit}&offset={offset}")

    def get_customer_summary(self) -> dict[str, Any]:
        return self._get("/api/v1/analytics/customers/summary")
