from __future__ import annotations

from datetime import datetime
from typing import Any

from app.core.logger import logger
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.room import Room
from app.models.section import Section
from app.models.source_file import SourceFile
from app.models.timetable_entry import TimetableEntry


class TimetableRepository:
    def __init__(self, session: Any):
        self.session = session

    def save(self, records: list[dict[str, Any]], source_file: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        saved_records: list[dict[str, Any]] = []

        for record in records:
            entry = dict(record)
            if source_file is not None:
                entry["source_file"] = dict(source_file)
            saved_records.append(entry)

        if self.session is None:
            return saved_records

        try:
            source_record = None
            if source_file:
                source_record = SourceFile(
                    filename=str(source_file.get("filename", "unknown.xlsx")),
                    checksum=source_file.get("checksum"),
                    storage_path=source_file.get("storage_path"),
                    uploader=source_file.get("uploader"),
                    uploaded_at=datetime.utcnow(),
                )
                self.session.add(source_record)
                self.session.flush()

            for record in records:
                course = self._get_or_create_course(record)
                section = self._get_or_create_section(record, course)
                faculty = self._get_or_create_faculty(record)
                room = self._get_or_create_room(record)

                timetable_entry = TimetableEntry(
                    day=str(record.get("day", "Monday")),
                    start_time=str(record.get("start_time", record.get("time", "09:00")).split("-")[0]),
                    end_time=str(record.get("end_time", record.get("time", "10:00")).split("-")[-1]),
                    course_id=course.id,
                    section_id=section.id,
                    faculty_id=faculty.id,
                    room_id=room.id,
                    source_file_id=source_record.id if source_record else None,
                    slot_index=record.get("slot_index"),
                    created_at=datetime.utcnow(),
                )
                self.session.add(timetable_entry)

            self.session.commit()
            logger.info("persisted timetable records", extra={"count": len(records)})
        except Exception:
            self.session.rollback()
            raise

        return saved_records

    def _get_or_create_course(self, record: dict[str, Any]) -> Course:
        code = str(record.get("course_code") or "").strip() or None
        name = str(record.get("course_name") or "").strip()
        course = self.session.query(Course).filter(Course.name == name).one_or_none()
        if course is None:
            course = Course(code=code, name=name, kind=str(record.get("course_kind", "Course")))
            self.session.add(course)
            self.session.flush()
        return course

    def _get_or_create_section(self, record: dict[str, Any], course: Course) -> Section:
        code = str(record.get("section") or "").strip().upper()
        section = self.session.query(Section).filter(Section.code == code, Section.course_id == course.id).one_or_none()
        if section is None:
            section = Section(code=code, course_id=course.id)
            self.session.add(section)
            self.session.flush()
        return section

    def _get_or_create_faculty(self, record: dict[str, Any]) -> Faculty:
        faculty_name = str(record.get("faculty") or "").strip()
        faculty = self.session.query(Faculty).filter(Faculty.name == faculty_name).one_or_none()
        if faculty is None:
            faculty = Faculty(name=faculty_name)
            self.session.add(faculty)
            self.session.flush()
        return faculty

    def _get_or_create_room(self, record: dict[str, Any]) -> Room:
        room_name = str(record.get("room") or "").strip().upper()
        room = self.session.query(Room).filter(Room.name == room_name).one_or_none()
        if room is None:
            room = Room(name=room_name, building=str(record.get("building") or "").strip() or None)
            self.session.add(room)
            self.session.flush()
        return room
