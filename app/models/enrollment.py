from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base



class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    enrolled_at = Column(DateTime, server_default=func.now())
    progress = Column(Integer, default=0)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    paymentStatus=Column(Integer,default=0)  # 0 for unpaid, 1 for paid
