from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_customer_cohorts_endpoint_should_return_cohorts() -> None:
    response = client.get("/api/v1/analytics/cohorts")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]

    assert "cohort_month" in first
    assert "months_since_first_purchase" in first
    assert "customers" in first
    assert "retained_customers" in first
    assert "retention_rate" in first

    assert first["months_since_first_purchase"] >= 0
    assert first["customers"] > 0
    assert first["retained_customers"] >= 0
    assert 0 <= first["retention_rate"] <= 100
