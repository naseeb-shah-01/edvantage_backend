from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.lesson import LessonCreate, LessonResponse
from app.services.lesson_service import LessonService
from sqlalchemy.orm import Session
from app.db.session import get_db
router = APIRouter()

@router.post("/add", status_code=status.HTTP_201_CREATED, summary="Add a lesson to a section", description="Add a new lesson to an existing course section. Only instructors and admins can add lessons.")
async def add_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    try:
        lesson_service = LessonService(db).create_lesson(lesson)
        return lesson_service
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



