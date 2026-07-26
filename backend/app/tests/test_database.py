from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal, check_database_connection
from app.main import app


def test_database_session_creation():
    session = SessionLocal()
    assert session.bind is not None
    session.close()


def test_database_connection_check_handles_unavailable_database(monkeypatch):
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def execute(self, *_args, **_kwargs):
            raise SQLAlchemyError("connection unavailable")

    monkeypatch.setattr("app.core.database.SessionLocal", FakeSession)

    assert check_database_connection() is False


def test_health_endpoint_reports_database_status():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code in {200, 503}

    if response.status_code == 200:
        payload = response.json()
        assert payload["status"] == "ok"
        assert payload["database"] == "connected"
        assert payload["environment"] == "development"
    else:
        payload = response.json()
        assert payload["detail"] == "Database connection failed."
