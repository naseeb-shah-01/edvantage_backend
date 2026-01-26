from pydantic import BaseModel, Field

class Lesson(BaseModel):
    title: str
    title: str
    section_id: int
    duration_minutes: int = Field(..., gt=0, description="Duration of the lesson in minutes")
    video_url: str
    is_free_preview: bool = Field(False, description="Indicates if the lesson is available as a free preview")

class LessonCreate(Lesson):
    pass
class LessonResponse(Lesson):
    id: int
