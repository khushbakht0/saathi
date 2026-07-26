from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db


def test_get_db_yields_and_closes_session() -> None:
    db_generator = get_db()
    db = next(db_generator)

    assert isinstance(db, Session)
    assert db.bind is not None

    db_generator.close()

    assert db is not None


def test_database_session_executes_select_one() -> None:
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).scalar_one()
        assert result == 1
    finally:
        db.close()
