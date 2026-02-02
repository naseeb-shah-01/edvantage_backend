from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)

    is_primary = Column(Boolean, default=True)
    address_type = Column(String(50), default="home")  # home / office / billing

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="addresses")
