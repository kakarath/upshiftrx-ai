from fastapi.testclient import TestClient

from api.index import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "healthy"
    assert payload.get("service") == "upshiftrx-api"