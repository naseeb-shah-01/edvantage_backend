

from  app.models.coursesection import CourseSection



class CourseSectionService:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_section(self, course_section):
        new_section = CourseSection(
            title=course_section.title,
            description=course_section.description,
            course_id=course_section.course_id,
            order=course_section.order
        )
        self.db_session.add(new_section)
        self.db_session.commit()
        self.db_session.refresh(new_section)
        return new_section
