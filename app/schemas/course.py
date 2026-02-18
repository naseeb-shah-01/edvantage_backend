from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.lesson import LessonResponse
from app.schemas.user import UserResponse


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: int
    duration: Optional[str]  
    is_published: bool = False

    outcomes: Optional[List[str]] = None
    curriculum: Optional[List[str]] = None
    target_audience: Optional[List[str]] = None
    
    videoUrl:Optional[str] = None
    thumbUrl:Optional[str]=None
    
    image:Optional[str]=None
    r_pay:Optional[str]=None
    d_pay:Optional[str]=None
    domain:Optional[str]=None
    for_mat:Optional[str]=None
    certificate:bool
    brochure:Optional[str]=None
    d_price:int
    level:Optional[str]=None
    overview:str
    


class CourseCreate(CourseBase):
    title: str = Field(..., min_length=2, max_length=255)
    instructor_id: int
    price: int = Field(..., ge=0)

class CourseResponse(CourseBase):
    id: int
    instructor_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CourseBulkCreateResponse(BaseModel):
    message: str
    count: int
    data: List[CourseResponse]




class AllCourses(BaseModel):
    courses: list[CourseResponse]
class CourseSectionResponse(BaseModel):
    id: int
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
class CourseWithName(BaseModel):
    id: int
    title: str
    

    class Config:
        from_attributes = True