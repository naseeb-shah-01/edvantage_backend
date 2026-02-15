from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentOut
from typing import List
from sqlalchemy.orm import joinedload
from app.models.progress import Progress
from app.services.progress_service import ProgressService
from app.models.coursesection import CourseSection
from app.services.progress_mapper import ProgressMapperService
from app.models.course import Course
class EnrollService:
    def __init__(self, db_session):
        self.db_session = db_session

    def enroll_user(self, user_id: int, course_id: int) -> Enrollment:
        # Check if the user is already enrolled in the course
        # existing_enrollment = (
        #     self.db_session.query(Enrollment)
        #     .filter_by(user_id=user_id, course_id=course_id)
        #     .first()
        # )
        # if existing_enrollment:
        #     raise ValueError(f"User {user_id} is already enrolled in course {course_id}")

        # Create a new enrollment record
        new_enrollment = Enrollment(user_id=user_id, course_id=course_id)
        self.db_session.add(new_enrollment)
        self.db_session.commit()
        self.db_session.refresh(new_enrollment)
        # Initialize progress tracking for the enrolled user
        progress_service = ProgressService(self.db_session)
        progress_service.createProgressViaCourseId(user_id, course_id,new_enrollment.id)


        

        return new_enrollment

    def get_enrollment_with_course(self, user_id: int) ->List[EnrollmentOut ]:
        enrollments = (
            self.db_session.query(Enrollment)
            .filter_by(user_id=user_id).options(
                joinedload(Enrollment.course)  
            )
            .all()
        )
        
        return enrollments  

    

    def get_enrollment_by_id(self, enrollment_id: int):
        enrollment = (
            self.db_session
            .query(Enrollment)
            .options(
                joinedload(Enrollment.course)
                    .joinedload(Course.sections),
                joinedload(Enrollment.progress_records)
            )
            .filter(Enrollment.id == enrollment_id)
            .first()
        )

        if not enrollment:
            return None

        progress_mapper = ProgressMapperService(enrollment)
        mapped_progress = progress_mapper.map_progress()

        return {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "enrolled_at": enrollment.enrolled_at,
            "progress": enrollment.progress,
            "paymentStatus": enrollment.paymentStatus,
            "course": enrollment.course,
            "progress_records": mapped_progress
        }

