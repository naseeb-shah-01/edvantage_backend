from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime   



class CourseSection(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: int
    order: int

class CourseSectionCreate(CourseSection):
    pass
class CourseSectionResponse(CourseSection):
    id: int
    created_at: datetime
    

    class Config:
        
        from_attributes=True





