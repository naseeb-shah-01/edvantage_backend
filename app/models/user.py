from sqlalchemy import Column, Integer, String, Boolean, DateTime,Enum
from sqlalchemy.sql import func
from app.db.session import Base 
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.dialects.postgresql import JSONB

 # ✅ IMPORT SAME BASE




class UserRole(str, enum.Enum):
    admin = "admin"
    instructor = "instructor"
    student = "student"

class UserType(str,enum.Enum):
    student="student"
    professional="professional"
    
 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    full_name = Column(String, nullable=False)
    contact=Column(String, nullable=True)
    expertise=Column(JSONB, nullable=True)
    whatsapp=Column(String, nullable=True)
    collage=Column(String, nullable=True)
    interest=Column(JSONB,nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    user_type = Column(Enum(UserType,name="user_type"),nullable=False)

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
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
