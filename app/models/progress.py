from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)

    # REQUIRED: every progress belongs to a course enrollment
    enrollment_id = Column(
        Integer,
        ForeignKey("enrollments.id", ondelete="CASCADE"),
        nullable=False
    )

    # polymorphic fields
    trackable_type = Column(
        String(10),  # "lesson" | "section"
        nullable=False
    )

    trackable_id = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="in_progress"
    )

    completed_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # relationships
    enrollment = relationship("Enrollment", backref="progress_records")

    __table_args__ = (
        UniqueConstraint(
            "id",
            "trackable_type",
            "trackable_id",
            name="uq_progress_enrollment_trackable"
        ),
    )
