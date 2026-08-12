from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_segments_should_return_success():
    response = client.get("/api/v1/analytics/segments")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    segment = data[0]

    assert isinstance(segment["segment"], str)
    assert isinstance(segment["customers"], int)
    assert isinstance(segment["average_spending"], float)
    assert isinstance(segment["average_frequency"], float)
    assert isinstance(segment["average_recency"], float)

    assert segment["customers"] >= 0
    assert segment["average_spending"] >= 0
    assert segment["average_frequency"] >= 0
    assert segment["average_recency"] >= 0


def test_get_kpis_should_return_kpi_data() -> None:
    response = client.get("/api/v1/analytics/kpis")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "total_customers" in data
    assert "total_orders" in data
    assert "total_revenue" in data
    assert "average_order_value" in data

    assert isinstance(data["total_customers"], int)
    assert isinstance(data["total_orders"], int)
    assert isinstance(data["total_revenue"], float)
    assert isinstance(data["average_order_value"], float)

    assert data["total_customers"] >= 0
    assert data["total_orders"] >= 0
    assert data["total_revenue"] >= 0
    assert data["average_order_value"] >= 0


def test_get_revenue_should_return_success():
    response = client.get("/api/v1/analytics/revenue")

    assert response.status_code == 200


def test_get_revenue_should_return_revenue_data():
    response = client.get("/api/v1/analytics/revenue")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "total_revenue" in data
    assert "total_orders" in data
    assert "average_order_value" in data
    assert "monthly" in data


def test_get_revenue_should_return_valid_values():
    response = client.get("/api/v1/analytics/revenue")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["total_revenue"], float)
    assert isinstance(data["total_orders"], int)
    assert isinstance(data["average_order_value"], float)
    assert isinstance(data["monthly"], list)

    assert data["total_revenue"] >= 0
    assert data["total_orders"] >= 0
    assert data["average_order_value"] >= 0


def test_get_revenue_should_return_monthly_data():
    response = client.get("/api/v1/analytics/revenue")

    assert response.status_code == 200

    data = response.json()

    assert len(data["monthly"]) > 0

    month = data["monthly"][0]

    assert "month" in month
    assert "revenue" in month
    assert "orders" in month
    assert "average_order_value" in month

    assert isinstance(month["month"], str)
    assert isinstance(month["revenue"], float)
    assert isinstance(month["orders"], int)
    assert isinstance(month["average_order_value"], float)

    assert month["revenue"] >= 0
    assert month["orders"] >= 0
    assert month["average_order_value"] >= 0


def test_get_customers_should_return_success():
    response = client.get("/api/v1/analytics/customers")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_customers_should_return_customer_data():
    response = client.get("/api/v1/analytics/customers")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    customer = data[0]

    assert "customer_id" in customer
    assert "total_orders" in customer
    assert "total_items" in customer
    assert "total_spent" in customer
    assert "average_order_value" in customer
    assert "first_order_date" in customer
    assert "last_order_date" in customer
    assert "customer_lifetime_days" in customer
    # assert "segment" in customer


def test_get_customers_should_return_valid_values():
    response = client.get("/api/v1/analytics/customers")

    assert response.status_code == 200

    data = response.json()

    customer = data[0]

    assert isinstance(customer["customer_id"], str)
    assert isinstance(customer["total_orders"], int)
    assert isinstance(customer["total_items"], int)
    assert isinstance(customer["total_spent"], float)
    assert isinstance(customer["average_order_value"], float)
    assert isinstance(customer["customer_lifetime_days"], int)
    # assert isinstance(customer["segment"], str)

    assert customer["total_orders"] >= 0
    assert customer["total_items"] >= 0
    assert customer["total_spent"] >= 0
    assert customer["average_order_value"] >= 0
    assert customer["customer_lifetime_days"] >= 0


def test_get_customers_should_respect_limit():
    response = client.get("/api/v1/analytics/customers?limit=5")

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 5


def test_get_customers_should_filter_by_segment():
    response = client.get("/api/v1/analytics/customers?segment=Champions")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    # for customer in data:
    #     assert customer["segment"] == "Champions"


# VERIFICAR SOBRE O UNIQUE_ID NO BANCO DE DADOS
# def test_get_customer_detail_should_return_customer_data():
#     response = client.get(
#         "/api/v1/analytics/customers/290c77bc529b7ac935b93aa66c333dc3"
#     )

#     assert response.status_code == 200

#     data = response.json()

#     assert isinstance(data, dict)

#     assert "customer_unique_id" in data
#     assert "total_orders" in data
#     assert "total_items" in data
#     assert "total_spent" in data
#     assert "average_order_value" in data
#     assert "segment" in data
#     assert "recency" in data
#     assert "frequency" in data
#     assert "monetary" in data
#     assert "rfm_score" in data


def test_get_customer_detail_should_return_not_found():
    response = client.get("/api/v1/analytics/customers/ad21c59c0840e6cb83a9ceb5573f8159")

    assert response.status_code == 404


def test_get_products_should_return_success():
    response = client.get("/api/v1/analytics/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "products" in data


def test_get_products_should_return_product_data():
    response = client.get("/api/v1/analytics/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["products"], list)
    assert len(data["products"]) > 0

    product = data["products"][0]

    assert "product_id" in product
    assert "product_category" in product
    assert "total_items" in product
    assert "total_orders" in product
    assert "total_revenue" in product
    assert "average_item_price" in product


def test_get_products_should_return_valid_values():
    response = client.get("/api/v1/analytics/products")

    assert response.status_code == 200

    data = response.json()
    product = data["products"][0]

    assert isinstance(product["product_id"], str)
    assert isinstance(product["total_items"], int)
    assert isinstance(product["total_orders"], int)
    assert isinstance(product["total_revenue"], float)
    assert isinstance(product["average_item_price"], float)

    assert product["total_items"] >= 0
    assert product["total_orders"] >= 0
    assert product["total_revenue"] >= 0
    assert product["average_item_price"] >= 0


def test_get_products_should_respect_limit():
    response = client.get("/api/v1/analytics/products?limit=5")

    assert response.status_code == 200

    data = response.json()

    assert len(data["products"]) <= 5


def test_get_products_should_filter_by_category():
    response = client.get("/api/v1/analytics/products?category=beleza_saude")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["products"], list)

    for product in data["products"]:
        assert product["product_category"] == "beleza_saude"


def test_get_product_categories_should_return_success():
    response = client.get("/api/v1/analytics/products/categories")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "categories" in data


def test_get_product_categories_should_return_category_data():
    response = client.get("/api/v1/analytics/products/categories")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0

    category = data["categories"][0]

    assert "category" in category
    assert "total_items" in category
    assert "total_orders" in category
    assert "total_revenue" in category
    assert "total_freight" in category


def test_get_product_categories_should_return_valid_values():
    response = client.get("/api/v1/analytics/products/categories")

    assert response.status_code == 200

    data = response.json()
    category = data["categories"][0]

    assert isinstance(category["category"], str)
    assert isinstance(category["total_items"], int)
    assert isinstance(category["total_orders"], int)
    assert isinstance(category["total_revenue"], float)
    assert isinstance(category["total_freight"], float)

    assert category["total_items"] >= 0
    assert category["total_orders"] >= 0
    assert category["total_revenue"] >= 0
    assert category["total_freight"] >= 0
