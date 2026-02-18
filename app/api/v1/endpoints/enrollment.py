from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse,EnrollmentOut,EnrollmentWithUserDetails
from app.db.session import get_db
from app.services.enroll_service import EnrollService
from app.services.email import send_email_service
from typing import List
from fastapi import BackgroundTasks


router = APIRouter()

@router.post("/user", response_model=EnrollmentResponse, status_code=201, summary="Enroll a user in a course", description="Enroll a user in a specified course.")
async def enroll_user(data:EnrollmentCreate,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Logic to enroll a user in a course
    user_id = data.user_id
    course_id = data.course_id
    
    enroll_service = EnrollService(db)
    try:
        enrollment = enroll_service.enroll_user(user_id, course_id)
        background_tasks.add_task(
    send_email_service,   # 👈 NO ()
    data.email,
    "Enrollment Confirmation",
    "enrollmentTemplate",
    {
        "studentName": data.user_name,
        "courseName":data.course_name,
        "enrollmentId":enrollment.id

        
    }
)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return enrollment

@router.get("enroll-id/{enrollment_id}", response_model=EnrollmentResponse, summary="Get enrollment details", description="Retrieve details of a specific enrollment by its ID.")
async def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    # Logic to get enrollment details
    enrollment = db.query(EnrollService).filter(EnrollService.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.get("/user/{user_id}/courses", response_model=List[EnrollmentOut], summary="Get user enrollments", description="Retrieve all courses a user is enrolled in.")
async def get_user_enrollments(user_id: int, db: Session = Depends(get_db)):
    # Logic to get all enrollments for a user
    enrollments = EnrollService(db).get_enrollment_with_course(user_id)
    return enrollments   



@router.get(
    "/course/{course_id}/users",
    response_model=List[EnrollmentWithUserDetails],
    summary="Get course enrollments",
    description="Retrieve all users enrolled in a specific course."
)
async def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db)
):
    try:
        enrollments = EnrollService(db).get_course_id_with_user_details(course_id)

        if not enrollments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No enrollments found for this course"
            )

        return enrollments

    except HTTPException:
        # re-raise HTTP exceptions
        raise

    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while fetching enrollments"
        )
