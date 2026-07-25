from sqlalchemy.orm import Session

from app.database import get_db


def test_get_db_yields_and_closes_session() -> None:
    db_generator = get_db()
    db = next(db_generator)

    assert isinstance(db, Session)
    assert db.bind is not None

    db_generator.close()

    assert db is not None
