from pathlib import Path

from openpyxl import Workbook

from app.services.parsers.excel_workbook_parser import ExcelWorkbookParser
from app.services.timetable_validation_service import TimetableValidationService
from app.services.timetable_normalization_service import TimetableNormalizationService
from app.repositories.timetable_repository import TimetableRepository
from app.main import app
from fastapi.testclient import TestClient


def create_sample_workbook(path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Class Timetable"
    ws.append(["Day", "Time", "Course Code", "Course Name", "Section", "Faculty", "Room", "Building", "Batch"])
    ws.append(["Monday", "09:00-10:00", "CS101", "Artificial Intelligence", "A", "Dr. Ali", "A-101", "Block A", "BSCS-1"])
    ws.append(["Tuesday", "11:00-12:00", "CS201", "Artificial Intelligence Lab", "B", "Dr. Zara", "LAB-2", "Block B", "BSCS-2"])
    wb.save(path)


def test_excel_parser_extracts_timetable_records(tmp_path: Path):
    workbook_path = tmp_path / "sample_timetable.xlsx"
    create_sample_workbook(workbook_path)

    parser = ExcelWorkbookParser()
    records = parser.parse(workbook_path)

    assert len(records) == 2
    assert records[0]["course_name"] == "Artificial Intelligence"
    assert records[0]["day"] == "Monday"


def test_validation_service_returns_structured_errors_for_invalid_payload():
    service = TimetableValidationService()
    payload = [
        {
            "day": "",
            "time": "25:00-26:00",
            "course_name": "",
            "room": "",
            "section": "A",
        }
    ]

    result = service.validate(payload)

    assert result.is_valid is False
    assert any("day" in error["field"] for error in result.errors)
    assert any("time" in error["field"] for error in result.errors)
    assert any("room" in error["field"] for error in result.errors)


def test_normalization_service_standardizes_course_values():
    service = TimetableNormalizationService()
    normalized = service.normalize(
        {
            "course_name": "Artificial Intelligence Lab",
            "section": "A",
            "faculty": "Dr. Ali",
            "room": "A-101",
        }
    )

    assert normalized["course_name"] == "Artificial Intelligence Lab"
    assert normalized["course_kind"] == "Lab"
    assert normalized["section"] == "A"


def test_repository_can_store_normalized_records_in_memory():
    repo = TimetableRepository(session=None)
    normalized = [
        {
            "course_name": "Artificial Intelligence",
            "course_code": "CS101",
            "section": "A",
            "faculty": "Dr. Ali",
            "room": "A-101",
            "batch": "BSCS-1",
        }
    ]

    saved = repo.save(normalized)
    assert len(saved) == 1
    assert saved[0]["course_name"] == "Artificial Intelligence"


def test_repository_preserves_original_file_metadata():
    repo = TimetableRepository(session=None)
    normalized = [
        {
            "course_name": "Artificial Intelligence",
            "course_code": "CS101",
            "section": "A",
            "faculty": "Dr. Ali",
            "room": "A-101",
            "batch": "BSCS-1",
        }
    ]

    saved = repo.save(normalized, source_file={"filename": "sample_timetable.xlsx", "checksum": "abc123"})
    assert len(saved) == 1
    assert saved[0]["source_file"]["filename"] == "sample_timetable.xlsx"
    assert saved[0]["source_file"]["checksum"] == "abc123"


def test_api_endpoint_accepts_timetable_payload():
    client = TestClient(app)
    response = client.post(
        "/api/timetable",
        json={
            "rows": [
                {
                    "day": "Monday",
                    "time": "09:00-10:00",
                    "course_code": "CS101",
                    "course_name": "Artificial Intelligence",
                    "section": "A",
                    "faculty": "Dr. Ali",
                    "room": "A-101",
                    "building": "Block A",
                    "batch": "BSCS-1",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Timetable payload normalized successfully."
