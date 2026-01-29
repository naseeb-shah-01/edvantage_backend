from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.schemas.lesson import LessonResponse
from app.schemas.user import UserResponse

class Course(BaseModel):
    
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    instructor_id: int
    price: int
    duration: Optional[int] = None  # duration in minutes
    is_published: bool
    created_at: datetime

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    instructor_id: int
    price: int = Field(..., ge=0)
    duration: Optional[int] = None 
    is_published: bool = False
class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    instructor_id: int
    price: int
    duration: Optional[int] = None 
    is_published: bool
    created_at: datetime

    class Config:
        orm_mode = True
class AllCourses(BaseModel):
    courses: list[CourseResponse]
class CourseSectionResponse(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: int
    order: int
    lessons: list[LessonResponse] 

    class Config:
        from_attributes = True

class CourseResponseWithSections(BaseModel):
    id: int
    title: str
    description: str | None
    category: str | None
    price: int
    is_free: bool
    is_published: bool
    duration: int | None
    created_at: datetime
    instructor:UserResponse
    
    sections: list[CourseSectionResponse]

    class Config:
        from_attributes = True
   