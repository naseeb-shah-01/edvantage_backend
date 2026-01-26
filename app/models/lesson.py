from sqlalchemy import Column, Integer, String, Text, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("course_sections.id"))

    title = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    duration_minutes = Column (Integer)

    is_free_preview = Column(Boolean, default=False)

    section = relationship("CourseSection", backref="lessons")
