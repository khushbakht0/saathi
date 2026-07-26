from fastapi.testclient import TestClient

from app.main import app


def test_startup_lifecycle_does_not_crash():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code in {200, 503}
