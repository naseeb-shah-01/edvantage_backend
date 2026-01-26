from fastapi import APIRouter
from app.api.v1.endpoints import auth, courses, coursesection, lesson, enrollment,admin

v1_router = APIRouter()

# Include all v1 endpoints
v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
v1_router.include_router(coursesection.router, prefix="/course-sections", tags=["Course Sections"])
v1_router.include_router(lesson.router, prefix="/lessons", tags=["Lessons"])
v1_router.include_router(enrollment.router, prefix="/enroll", tags=["Enrollment"])
v1_router.include_router(admin.admin_router, prefix="/admin", tags=["Admin"])