from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    day: Mapped[str] = mapped_column(String(20), nullable=False)
    start_time: Mapped[str] = mapped_column(String(20), nullable=False)
    end_time: Mapped[str] = mapped_column(String(20), nullable=False)
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id"), nullable=True, index=True)
    section_id: Mapped[int | None] = mapped_column(ForeignKey("sections.id"), nullable=True, index=True)
    faculty_id: Mapped[int | None] = mapped_column(ForeignKey("faculty.id"), nullable=True, index=True)
    room_id: Mapped[int | None] = mapped_column(ForeignKey("rooms.id"), nullable=True, index=True)
    source_file_id: Mapped[int | None] = mapped_column(ForeignKey("source_files.id"), nullable=True, index=True)
    slot_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    course = relationship("Course", backref="timetable_entries")
    section = relationship("Section", backref="timetable_entries")
    faculty = relationship("Faculty", backref="timetable_entries")
    room = relationship("Room", backref="timetable_entries")
    source_file = relationship("SourceFile", backref="timetable_entries")
