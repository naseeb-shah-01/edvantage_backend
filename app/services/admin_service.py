from sqlalchemy import func
from app.models.course import Course
from app.models.user import User
from app.models.enrollment import Enrollment


class AdminService:
    def __init__(self, db_session):
        self.db_session = db_session

    # ===== LIST METHODS (existing) =====
    def get_all_students(self) -> list[User]:
        return self.db_session.query(User).filter(User.role == "student").all()

    def get_all_instructors(self) -> list[User]:
        return self.db_session.query(User).filter(User.role == "instructor").all()

    def get_all_courses(self) -> list[Course]:
        return self.db_session.query(Course).all()

    def get_all_enrollments(self) -> list[Enrollment]:
        return self.db_session.query(Enrollment).all()

    # ===== COUNT METHODS (new) =====
    def get_students_count(self) -> int:
        return (
            self.db_session.query(func.count(User.id))
            .filter(User.role == "student")
            .scalar()
        )

    def get_instructors_count(self) -> int:
        return (
            self.db_session.query(func.count(User.id))
            .filter(User.role == "instructor")
            .scalar()
        )

    def get_courses_count(self) -> int:
        return self.db_session.query(func.count(Course.id)).scalar()

    def get_enrollments_count(self) -> int:
        return self.db_session.query(func.count(Enrollment.id)).scalar()

    # ===== DASHBOARD SUMMARY (recommended) =====
    def get_admin_dashboard_counts(self) -> dict:
        return {
            "students": self.get_students_count(),
            "instructors": self.get_instructors_count(),
            "courses": self.get_courses_count(),
            "enrollments": self.get_enrollments_count(),
        }
