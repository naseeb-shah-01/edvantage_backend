from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base fields for user"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: Optional[str] = "student"  # default role

class UserCreate(UserBase):
    """Data required to create a user"""
    password: str = Field(..., min_length=6, max_length=100)
    confirm_password: str
    
    # Check if passwords match
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return True

class UserResponse(UserBase):
    """What we send back to the user"""
    id: int
    is_active: bool
    created_at: datetime
    
    # This tells Pydantic to read from SQLAlchemy model
    class Config:
        from_attributes = True

# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str