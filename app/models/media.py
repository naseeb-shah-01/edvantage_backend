

from sqlalchemy import Column, Integer, ForeignKey, DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base



class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    public_id = Column(String,nullable=False)
    resource_type = Column(String,nullable=False)
    size=Column(Integer,nullable=True)

    