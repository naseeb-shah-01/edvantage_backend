from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentOut
from typing import List
from sqlalchemy.orm import joinedload

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

        return new_enrollment

    def get_enrollment_with_course(self, user_id: int) ->List[EnrollmentOut ]:
        enrollments = (
            self.db_session.query(Enrollment)
            .filter_by(user_id=user_id).options(
                joinedload(Enrollment.course)  
            )
            .all()
        )
        print("Fetched enrollments:", enrollments)
        return enrollments  