from app.services.timetable_service import TimetableService


def test_normalize_entries_handles_basic_payload():
    service = TimetableService()
    payload = {
        "rows": [
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "10:00",
                "subject": "Math",
                "room": "A-101",
                "source_type": "excel",
            }
        ]
    }

    entries = service.normalize_entries(payload)

    assert len(entries) == 1
    assert entries[0].subject == "Math"
    assert entries[0].room == "A-101"
