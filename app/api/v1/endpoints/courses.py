from fastapi import APIRouter, Depends, HTTPException, status,Depends
from app.schemas.course import CourseCreate, CourseResponse,AllCourses,CourseResponseWithSections,CourseBulkCreateResponse
from typing import List

router= APIRouter()
from sqlalchemy.orm import Session
from app.db.session import get_db

from  app.services.course_service import CourseService


@router.post(
    "/", 
        response_model=CourseBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course",
    description="Create a new course. Only instructors and admins can create courses."
)
async def create_courses(
    courses_data: List[CourseCreate],
    db: Session = Depends(get_db)
):
    try:
        instructor_id = 1  # TODO: replace with auth-based instructor ID

        created_courses = []
        for course_data in courses_data:
            course = CourseService.create_course(db, course_data, instructor_id)
            created_courses.append(course)

        return {
            "message": "Courses created successfully",
            "count": len(created_courses),
            "data": created_courses
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/all", response_model=list[CourseResponse], status_code=status.HTTP_200_OK,)
async def get_course_all( db: Session = Depends(get_db)):
    
    courses = CourseService.get_all_courses(db)
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found")
    return courses


@router.get("/all-details/{id}", response_model=CourseResponseWithSections, status_code=status.HTTP_200_OK,)
async def get_course(id: int, db: Session = Depends(get_db)):
    print("Fetching course with ID:", id)
    course = CourseService.get_course_with_sections_and_lessons(db, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course    
@router.get("/{id}", response_model=CourseResponse, status_code=status.HTTP_200_OK,)
async def get_course(id: int, db: Session = Depends(get_db)):
    print("Fetching course with ID:", id)
    course = CourseService.get_course(db, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course