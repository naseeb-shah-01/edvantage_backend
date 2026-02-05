from fastapi import APIRouter, Depends, HTTPException, status,File, UploadFile, Form
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.repositories.lessson import LessonRepository
from app.schemas.lesson import LessonCreate
from app.schemas.media import UploadResponse,StoreMediaEntry
from app.services.cloudinary_service import CloudinaryService
from app.repositories.media_repository import MediaRepository
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
@admin_router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form("fastapi_uploads"),
    resource_type: str = Form("auto"),db: Session = Depends(get_db)
):
    """
    Upload a file to Cloudinary
    
    - **file**: File to upload
    - **folder**: Cloudinary folder (default: "fastapi_uploads")
    - **resource_type**: Type of resource ('image', 'video', 'auto')
    """
    # Validate file type
    allowed_image_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"]
    allowed_video_types = ["video/mp4", "video/mov", "video/avi", "video/wmv", "video/flv"]
    
    content_type = file.content_type
    
    if resource_type == "image" and content_type not in allowed_image_types:
        raise HTTPException(status_code=400, detail="Invalid image file type")
    
    if resource_type == "video" and content_type not in allowed_video_types:
        raise HTTPException(status_code=400, detail="Invalid video file type")
    
    # Upload file
    result = await CloudinaryService.upload_file(file, folder, resource_type)
    media_data = StoreMediaEntry(
                public_id=result["public_id"],
                    resource_type=result["resource_type"],
                size=result["bytes"],
                )

    # ✅ Correct repo usage
    media_repo = MediaRepository(db)
    media_repo.createMedia(media_data)
    return result

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

@admin_router.post("/delete", tags=["Admin"])
async def delete_file(
    public_id:str,
    resource_type: str,
    db: Session = Depends(get_db)
):
    cloudinary_error = None

    # 1️⃣ Try Cloudinary delete (optional)
    try:
        await CloudinaryService.delete_file(
            public_id=public_id,
            resource_type=resource_type
        )
    except Exception as e:
        cloudinary_error = str(e)

    # 2️⃣ DB delete (MANDATORY)
    media_repo = MediaRepository(db)
    deleted = media_repo.delete_file(public_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Media not found in database"
        )

    return {
        "message": "Delete completed",
        "public_id": public_id,
        "cloudinary_deleted": cloudinary_error is None,
        "cloudinary_error": cloudinary_error
    }

