from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)

    instructor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    instructor = relationship(
        "User",
        back_populates="courses"
    )

    price = Column(Integer, nullable=False, default=0)
    duration = Column(Integer, nullable=True)  # minutes
    is_published = Column(Boolean, default=False)
    is_free = Column(Boolean, default=False)

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, server_default=func.now())

    # -------------------------
    # 🔹 JSON FIELDS (APPLIED)
    # -------------------------

    outcomes = Column(JSONB, nullable=True)          # list[str]
    curriculum = Column(JSONB, nullable=True)        # list[str]
    target_audience = Column(JSONB, nullable=True)   # list[str]
