from app.services.email_service import EmailService


def test_classify_email_returns_expected_shape():
    service = EmailService()
    result = service.classify_email("CS101 Lecture", "Class is at 10:00")

    assert result["classification"] == "timetable"
    assert result["confidence"] > 0
    assert result["model"] == "gpt-4o-mini"
