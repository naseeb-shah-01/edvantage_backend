from sqlalchemy import Column, Integer, String, Boolean, DateTime,Enum
from sqlalchemy.sql import func
from app.db.session import Base 
from sqlalchemy.orm import relationship
import enum

 # ✅ IMPORT SAME BASE

print("User model loaded")
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    instructor = "instructor"
    student = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    courses = relationship(
        "Course",
        back_populates="instructor",
        cascade="all, delete"
    )
    role = Column(
        Enum(UserRole, name="user_role"),
        default=UserRole.student,
        nullable=False
    )
    enrollments = relationship(
        "Enrollment",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
