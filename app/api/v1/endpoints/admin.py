from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import UserService
from app.services.admin_service import AdminService

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

            