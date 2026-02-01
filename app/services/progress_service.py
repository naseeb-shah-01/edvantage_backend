from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressResponse


from app.models.coursesection import CourseSection




class ProgressService:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_progress(self, user_id: int, lesson_id: int) -> Progress:
        new_progress = Progress(user_id=user_id, lesson_id=lesson_id)
        self.db_session.add(new_progress)
        self.db_session.commit()
        self.db_session.refresh(new_progress)
        return new_progress

    def get_user_progress(self, user_id: int):
        progress_records = (
            self.db_session.query(Progress)
            .filter_by(user_id=user_id)
            .all()
        )
        return progress_records

    def createProgressViaCourseId(self, user_id: int, course_id: int,enrollment_id:int):
        from app.models.lesson import Lesson

        lessons = (
            self.db_session.query(Lesson)
            .filter_by(id=course_id)
            .all()
        )
        section=(
            self.db_session.query(CourseSection)
            .filter_by(course_id=course_id)
            .all()
        )

        progress_records:list[ ProgressCreate] = []
        for lesson in lessons:
            progress = Progress(
                enrollment_id=enrollment_id,
                trackable_type='lesson',
                trackable_id=lesson.id
            )
            self.db_session.add(progress)
            progress_records.append(progress)
        for sec in section:
            progress = Progress(
                enrollment_id=enrollment_id,
                trackable_type='section',
                trackable_id=sec.id
            )
            self.db_session.add(progress)
            progress_records.append(progress)
   
        self.db_session.commit()
        for progress in progress_records:
            self.db_session.refresh(progress)

        return progress_records