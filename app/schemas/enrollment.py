from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user import UserResponseWithOutAddress

from datetime import datetime
class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    instructor_id: int
    price: int
    duration: Optional[str]
    is_published: bool
    is_free: bool
    created_at: datetime
    image: Optional[str]

    class Config:
        from_attributes = True
class Enrollment(BaseModel):
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: int = Field(0, ge=0, le=100)  # progress percentage

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int
    user_name:str
    email:str
    course_name:str
class EnrollmentResponse(Enrollment):
    id: int

    class Config:
        orm_mode = True
class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    progress: int
    enrolled_at: datetime
    course: CourseOut   # 👈 nested course

    class Config:
        from_attributes = True
class EnrollmentWithUserDetails(BaseModel):
    id: int
    course_id: int
    progress: int
    enrolled_at: datetime
    user: UserResponseWithOutAddress   # 👈 nested user details

    class Config:
        from_attributes = True