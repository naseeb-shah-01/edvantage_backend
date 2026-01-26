from fastapi import APIRouter, Depends, HTTPException, status,Depends
from app.schemas.course_section import CourseSectionCreate, CourseSectionResponse
from app.services.course_section_service import CourseSectionService

router= APIRouter()
from sqlalchemy.orm import Session
from app.db.session import get_db

from  app.services.course_service import CourseService




@router.post("/add", status_code=status.HTTP_201_CREATED,summary="Add a section to a course", description="Add a new section to an existing course. Only instructors and admins can add sections.")
async def add_course_section( section:CourseSectionCreate , db: Session = Depends(get_db)):
    try:
       
        
        course_section_service = CourseSectionService(db).create_section(section)
        return course_section_service
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    