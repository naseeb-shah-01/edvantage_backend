
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate


class LessonRepository:
    def __init__(self, db_session):
         
        self.db_session = db_session
    def createLesson(self, data:LessonCreate) -> Lesson:
        payload = data.model_dump()
        payload["lesson_type"] = payload["lesson_type"].value  # 👈 FIX

        new_lesson = Lesson(**payload)

        self.db_session.add(new_lesson)
        self.db_session.commit()
        self.db_session.refresh(new_lesson)
        return new_lesson
    def getAllLessons(self, id:int) -> list[Lesson]:
        lessons = (
            self.db_session.query(Lesson)
            .filter_by(section_id=id)
            .all()
        )
        return lessons