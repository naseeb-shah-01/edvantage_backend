from fastapi import APIRouter, Depends, HTTPException, status,Request
from app.models.progress import Progress

from app.db.session import get_db
from app.services.enroll_service import EnrollService


from app.schemas.progress import ProgressCreate, ProgressResponse


from app.services.progress_service import ProgressService


router = APIRouter()
@router.get("/enrollment/course-details/{enrollment_id}", summary="Get course details by enrollment ID", description="Retrieve course progress details for a specific enrollment ID.")
def getCourseDetailsByEnrollmentId(request:Request,enrollment_id: int,db = Depends(get_db)):
    
    enroll=EnrollService(db).get_enrollment_by_id(enrollment_id)
    print("Enrollment fetched:", enroll)
    return enroll