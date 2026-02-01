from pydantic import BaseModel, Field



class Progress(BaseModel):
    enrollment_id: int
    trackable_type: str = Field(..., description='Type of the trackable item, e.g., "lesson" or "section"')
    trackable_id: int

class ProgressCreate(Progress):
    pass
class ProgressResponse(Progress):
    id: int
    status: str
    completed_at: str | None
    created_at: str

    class Config:
        orm_mode = True