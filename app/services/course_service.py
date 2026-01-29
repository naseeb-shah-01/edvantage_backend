from sqlalchemy.orm import Session,joinedload
from slugify import slugify

from app.models.course import Course
from app.schemas.course import CourseCreate
from app.models.coursesection import CourseSection

class CourseService:

    @staticmethod
    def generate_slug(title: str, db: Session) -> str:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while db.query(Course).filter(Course.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug
    @staticmethod
    def get_course(db: Session, course_id: int) -> Course | None:
        print("Inside CourseService.get_course with course_id:", course_id)
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_all_courses(db: Session) -> list[Course]:
        return db.query(Course).all()


     
    @staticmethod
    def get_course_with_sections_and_lessons(db: Session, course_id: int):
        course = (
            db.query(Course)
            .options(
                joinedload(Course.instructor),
                joinedload(Course.sections).
                    joinedload(CourseSection.lessons)  # ✅ FIXED
            )
            .filter(Course.id == course_id)
            .first()
        )

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        return course   
    @staticmethod
    def create_course(
        db: Session,
        course_data: CourseCreate,
        instructor_id: int
    ) -> Course:
        
        # 2. Convert request data to dict
        course_dict = course_data.dict()
        course_dict.pop("instructor_id", None)

        # 3. Create Course object
        course = Course(
            **course_dict,
          
            instructor_id=instructor_id,
            is_free=(course_data.price == 0)
        )

        # 4. Save to database
        db.add(course)
        db.commit()
        db.refresh(course)

        return course
