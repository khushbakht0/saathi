from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_timetable_endpoint_returns_200():
    payload = {
        "rows": [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "10:00",
                "subject": "Computer Science",
                "room": "B-12",
                "source_type": "excel",
            }
        ]
    }

    response = client.post("/api/timetable", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Timetable payload normalized successfully."
