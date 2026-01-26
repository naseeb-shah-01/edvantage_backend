from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class CourseSection(Base):
    __tablename__ = "course_sections"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))

    title = Column(String, nullable=False)
    order = Column(Integer)
    description=Column(String, nullable=True)

    course = relationship("Course", backref="sections")
