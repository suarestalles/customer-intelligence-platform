from typing import Final

OLIST_BASE_URL: Final = (
    "https://huggingface.co/datasets/"
    "miminmoons/"
    "olist-ecommerce-for-delivery-and-review-prediction/"
    "resolve/main/data"
)

CUSTOMERS_URL: Final = f"{OLIST_BASE_URL}/olist_customers_dataset.csv"
ORDERS_URL: Final = f"{OLIST_BASE_URL}/olist_orders_dataset.csv"
ORDER_ITEMS_URL: Final = f"{OLIST_BASE_URL}/olist_order_items_dataset.csv"
ORDER_PAYMENTS_URL: Final = f"{OLIST_BASE_URL}/olist_order_payments_dataset.csv"
ORDER_REVIEWS_URL: Final = f"{OLIST_BASE_URL}/olist_order_reviews_dataset.csv"
PRODUCTS_URL: Final = f"{OLIST_BASE_URL}/olist_products_dataset.csv"
SELLERS_URL: Final = f"{OLIST_BASE_URL}/olist_sellers_dataset.csv"
GEOLOCATION_URL: Final = f"{OLIST_BASE_URL}/olist_geolocation_dataset.csv"
CATEGORY_TRANSLATION_URL: Final = f"{OLIST_BASE_URL}/product_category_name_translation.csv"
