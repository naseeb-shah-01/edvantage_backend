from pydantic import BaseModel, EmailStr, Field

from typing import Optional,List
from datetime import datetime
import enum
from app.schemas.address import AddressCreate, AddressResponse

class UserRole(str, enum.Enum):
    admin = "admin"
    instructor = "instructor"
    student = "student"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str

    contact: Optional[str] = None
    whatsapp: Optional[str] = None
    collage: Optional[str] = None
    expertise: Optional[list[str]] = None

    role: Optional[UserRole] = UserRole.student

    # ✅ Address on signup
    addresses: Optional[List[AddressCreate]] = None
# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    contact: Optional[str]
    whatsapp: Optional[str]
    collage: Optional[str]
    expertise: Optional[list[str]]

    role: UserRole
    is_active: bool
    created_at: datetime

    addresses: List[AddressResponse] = []
    access_token: Optional[str] 
    

    class Config:
        orm_mode = True
