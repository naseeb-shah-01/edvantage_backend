
from app.models.lesson import Lesson


class LessonService:
    def __init__(self, db_session):
        self.db_session = db_session
    def create_lesson(self, lesson):
        lesson= lesson.dict()
        new_lesson = Lesson(
            **lesson
        )
        self.db_session.add(new_lesson)
        self.db_session.commit()
        self.db_session.refresh(new_lesson)
        return new_lesson
