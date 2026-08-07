from pipelines.ingestion.models import Dataset, DatasetFile
from pipelines.ingestion.sources import (
    CATEGORY_TRANSLATION_URL,
    CUSTOMERS_URL,
    GEOLOCATION_URL,
    ORDER_ITEMS_URL,
    ORDER_PAYMENTS_URL,
    ORDER_REVIEWS_URL,
    ORDERS_URL,
    PRODUCTS_URL,
    SELLERS_URL,
)

OLIST = Dataset(
    name="olist",
    description="Brazilian E-Commerce Public Dataset",
    files=(
        DatasetFile(
            name="olist_customer_dataset.csv", description="Customer information", url=CUSTOMERS_URL
        ),
        DatasetFile(
            name="olist_orders_dataset.csv",
            description="Orders",
            url=ORDERS_URL,
        ),
        DatasetFile(
            name="olist_order_items_dataset.csv",
            description="Order Items",
            url=ORDER_ITEMS_URL,
        ),
        DatasetFile(
            name="olist_order_payments_dataset.csv",
            description="Payments",
            url=ORDER_PAYMENTS_URL,
        ),
        DatasetFile(
            name="olist_order_reviews_dataset.csv",
            description="Reviews",
            url=ORDER_REVIEWS_URL,
        ),
        DatasetFile(
            name="olist_products_dataset.csv",
            description="Products",
            url=PRODUCTS_URL,
        ),
        DatasetFile(
            name="olist_sellers_dataset.csv",
            description="Sellers",
            url=SELLERS_URL,
        ),
        DatasetFile(
            name="olist_geolocation_dataset.csv",
            description="Geolocation",
            url=GEOLOCATION_URL,
        ),
        DatasetFile(
            name="product_category_name_translation.csv",
            description="Category Translation",
            url=CATEGORY_TRANSLATION_URL,
        ),
    ),
)

DATASETS = {
    OLIST.name: OLIST,
}
