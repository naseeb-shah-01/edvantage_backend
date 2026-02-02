from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class AddressBase(BaseModel):
    address_line_1: str = Field(..., max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str
    state: str
    country: str
    postal_code: str
    address_type: Optional[str] = "home"
    is_primary: Optional[bool] = True

class AddressCreate(AddressBase):
    pass
class AddressResponse(AddressBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
