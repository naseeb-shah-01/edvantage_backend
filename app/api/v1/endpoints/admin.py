from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.repositories.lessson import LessonRepository
from app.schemas.lesson import LessonCreate

from app.db.session import get_db 



admin_router = APIRouter()

@admin_router.get("/all/student", response_model=list[UserResponse], status_code=status.HTTP_200_OK, tags=["Admin"],summary="Get all users", description="Retrieve a list of all registered users. Admin access required.")
async def get_all_users(db: Session = Depends(get_db)):
    """Retrieve all users from the database"""
    try:
        users = UserService(db).get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@admin_router.get("/dashboard", status_code=status.HTTP_200_OK, tags=["Admin"],summary="Admin Dashboard", description="Access the admin dashboard. Admin access required.")
async def admin_dashboard(db: Session = Depends(get_db)):
    """Retrieve admin dashboard summary counts"""
    try:
        dashboard_counts = AdminService(db).get_admin_dashboard_counts()
        return dashboard_counts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@admin_router.post("/create/lesson", status_code=status.HTTP_201_CREATED, tags=["Admin"],summary="Create a new lesson", description="Create a new lesson in the system. Admin access required.")
async def create_lesson(lesson_data:LessonCreate, db: Session = Depends(get_db)):
    """Create a new lesson"""
    try:
        new_lesson = LessonRepository(db).createLesson(lesson_data)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@admin_router.get("/all/lessons/{id}", status_code=status.HTTP_200_OK, tags=["Admin"],summary="Get all lessons", description="Retrieve a list of all lessons. Admin access required.")   
async def get_all_lessons(id:int, db: Session = Depends(get_db)):
    """Retrieve all lessons"""
    try:
        lessons = LessonRepository(db).getAllLessons(id)
        return lessons
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))         