from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
import enum

class LessonType(enum.Enum):
    VIDEO = "VIDEO"
    TEXT = "TEXT"

class LessonCreate(BaseModel):
    section_id: int
    title: str
    lesson_type: LessonType

    video_url: Optional[HttpUrl] = None
    content: Optional[str] = None

    duration_minutes: Optional[int] = None
    is_free_preview: bool = False

    @field_validator("video_url")
    @classmethod
    def validate_video_url(cls, v, info):
        if info.data.get("lesson_type") == LessonType.VIDEO and not v:
            raise ValueError("video_url is required for video lessons")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v, info):
        if info.data.get("lesson_type") == LessonType.TEXT and not v:
            raise ValueError("content is required for text lessons")
        return v
class LessonResponse(BaseModel):
    id: int
    section_id: int
    title: str
    lesson_type: str
    video_url: Optional[str]
    content: Optional[str]

    duration_minutes: Optional[int]
    is_free_preview: bool

    class Config:
        from_attributes = True 
         # Pydantic v2