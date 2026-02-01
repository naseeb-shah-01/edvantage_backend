from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class LessonType(enum.Enum):
    VIDEO = "video"
    TEXT = "text"


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("course_sections.id"))

    title = Column(String, nullable=False)

    lesson_type = Column(Enum(LessonType), nullable=False)

    video_url = Column(String, nullable=True)        # only for VIDEO
    content = Column(Text, nullable=True)            # only for TEXT

    duration_minutes = Column(Integer, nullable=True)
    is_free_preview = Column(Boolean, default=False)

    section = relationship("CourseSection", backref="lessons")
