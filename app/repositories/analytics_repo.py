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
            ORDER BY average_recency DESC
        """

        return self.database.query(query)

    def get_customers(
        self,
        segment: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[tuple[Any, ...]]:
        query = """
            SELECT
                customer_unique_id,
                total_orders,
                total_items,
                total_spent,
                average_order_value,
                first_order_date,
                last_order_date,
                customer_lifetime_days
            FROM analytics.customer_metrics
        """

        params: list[Any] = []

        if segment:
            query = """
                SELECT
                    cm.customer_unique_id,
                    cm.total_orders,
                    cm.total_items,
                    cm.total_spent,
                    cm.average_order_value,
                    cm.first_order_date,
                    cm.last_order_date,
                    cm.customer_lifetime_days
                FROM analytics.customer_metrics AS cm
                INNER JOIN analytics.customer_rfm AS rfm
                    ON cm.customer_unique_id = rfm.customer_unique_id
                WHERE rfm.segment = ?
                ORDER BY cm.total_spent DESC
                LIMIT ? OFFSET ?
            """

            params = [segment, limit, offset]
        else:
            query += """
                ORDER BY total_spent DESC
                LIMIT ? OFFSET ?
            """

            params = [limit, offset]

        return self.database.query(query, params)

    def get_customer(self, customer_id: str) -> tuple[Any, ...] | None:
        query = """
            SELECT
                cm.customer_unique_id,
                cm.total_orders,
                cm.total_items,
                cm.total_spent,
                cm.average_order_value,
                cm.first_order_date,
                cm.last_order_date,
                cm.customer_lifetime_days,
                rfm.recency,
                rfm.frequency,
                rfm.monetary,
                rfm.recency_score,
                rfm.frequency_score,
                rfm.monetary_score,
                rfm.rfm_score,
                rfm.segment
            FROM analytics.customer_metrics AS cm
            LEFT JOIN analytics.customer_rfm AS rfm
                ON cm.customer_unique_id = rfm.customer_unique_id
            WHERE cm.customer_unique_id = ?
        """

        rows = self.database.query(query, [customer_id])

        return rows[0] if rows else None

    def get_kpis(self) -> tuple[Any, ...]:
        query = """
            SELECT
                COUNT(*) AS total_customers,
                SUM(total_orders) AS total_orders,
                SUM(total_spent) AS total_revenue,
                AVG(average_order_value) AS average_order_value
            FROM analytics.customer_metrics
        """

        rows = self.database.query(query)

        return rows[0]

    def get_revenue(self) -> tuple[Any, ...]:
        query = """
            SELECT
                COALESCE(SUM(om.payment_value), 0) AS total_revenue,
                COUNT(DISTINCT om.order_id) AS total_orders,
                COALESCE(
                    SUM(om.payment_value)
                    / NULLIF(COUNT(DISTINCT om.order_id), 0),
                    0
                ) AS average_order_value
            FROM analytics.order_metrics AS om
            LEFT JOIN raw.orders AS o
                ON om.order_id = o.order_id
            WHERE o.order_status = 'delivered'
        """

        rows = self.database.query(query)

        return rows[0]

    def get_monthly_revenue(self) -> list[tuple[Any, ...]]:
        query = """
            SELECT
                DATE_TRUNC(
                    'month',
                    om.order_purchase_timestamp
                ) AS month,
                SUM(om.payment_value) AS revenue,
                COUNT(DISTINCT om.order_id) AS orders,
                SUM(om.payment_value)
                    / NULLIF(COUNT(DISTINCT om.order_id), 0)
                    AS average_order_value
            FROM analytics.order_metrics AS om
            LEFT JOIN raw.orders AS o
                ON om.order_id = o.order_id
            WHERE o.order_status = 'delivered'
                AND om.order_purchase_timestamp IS NOT NULL
            GROUP BY 1
            ORDER BY 1
        """

        return self.database.query(query)

    def get_products(
        self,
        category: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[Any, ...]:
        where_clause = "WHERE o.order_status = 'delivered'"
        params: list[Any] = []

        if category:
            where_clause = "WHERE p.product_category_name = ?"
            params.append(category)

        summary_query = f"""
            SELECT
                COUNT(DISTINCT oi.product_id) AS total_products,
                COUNT(*) AS total_items,
                COALESCE(SUM(oi.price), 0) AS total_revenue
            FROM raw.order_items AS oi
            INNER JOIN raw.orders AS o
                ON oi.order_id = o.order_id
            INNER JOIN raw.products AS p
                ON oi.product_id = p.product_id
            {where_clause}
        """

        summary = self.database.query(summary_query, params)

        products_query = f"""
            SELECT
                oi.product_id,
                p.product_category_name,
                COUNT(*) AS total_items,
                COUNT(DISTINCT oi.order_id) AS total_orders,
                SUM(oi.price) AS total_revenue,
                SUM(oi.freight_value) AS total_freight,
                AVG(oi.price) AS average_item_price
            FROM raw.order_items AS oi
            INNER JOIN raw.orders AS o
                ON oi.order_id = o.order_id
            LEFT JOIN raw.products AS p
                ON oi.product_id = p.product_id
            {where_clause}
            GROUP BY
                oi.product_id,
                p.product_category_name
            ORDER BY total_revenue DESC
            LIMIT ? OFFSET ?
        """

        products = self.database.query(products_query, [*params, limit, offset])

        return summary[0], products

    def get_product_categories(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[Any, ...]:
        summary_query = """
            SELECT
                COUNT(DISTINCT p.product_category_name)
            FROM raw.order_items AS oi

            INNER JOIN raw.orders AS o
                ON oi.order_id = o.order_id

            LEFT JOIN raw.products AS p
                ON oi.product_id = p.product_id

            WHERE o.order_status = 'delivered'
                AND p.product_category_name IS NOT NULL
        """
        summary = self.database.query(summary_query)

        categories_query = """
            SELECT
                p.product_category_name AS category,
                COUNT(*) as total_items,
                COUNT(DISTINCT oi.order_id) AS total_orders,
                SUM(oi.price) AS total_revenue,
                SUM(oi.freight_value) AS total_freight
            FROM raw.order_items AS oi
            INNER JOIN raw.orders AS o
                ON oi.order_id = o.order_id
            LEFT JOIN raw.products AS p
                ON oi.product_id = p.product_id
            WHERE o.order_status = 'delivered'
            GROUP BY p.product_category_name
            ORDER BY total_revenue DESC
            LIMIT ? OFFSET ?
        """

        categories = self.database.query(categories_query, [limit, offset])

        return summary[0], categories

    def get_customer_summary(self) -> tuple[Any, ...]:
        query = """
            SELECT
                COUNT(*) AS total_customers,
                COALESCE(SUM(total_spent), 0) AS total_revenue,
                COALESCE(AVG(total_spent), 0) AS average_spend,
                COALESCE(AVG(total_orders), 0) AS average_orders
            FROM analytics.customer_metrics
        """

        rows = self.database.query(query)

        return rows[0]

    def get_customer_cohorts(self) -> list[tuple[Any, ...]]:
        query = """
            SELECT
                cohort_month,
                months_since_first_purchase,
                customers,
                retained_customers,
                retention_rate
            FROM analytics.customer_cohorts
            ORDER BY
                cohort_month,
                months_since_first_purchase
        """

        return self.database.query(query)
