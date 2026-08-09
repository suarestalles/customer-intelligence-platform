from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_segments_should_return_success():
    response = client.get("/api/v1/analytics/segments")

    assert response.status_code == 200


def test_get_segments_should_return_segment_data():
    response = client.get("/api/v1/analytics/segments")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    segment = data[0]

    assert "segment" in segment
    assert "customers" in segment
    assert "average_spending" in segment
    assert "average_frequency" in segment
    assert "average_recency" in segment
