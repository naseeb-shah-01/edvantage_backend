from  app.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session 

    def get_user_by_email(self, email: str) -> User | None:
        return self.db_session.query(User).filter(User.email == email).first()

    def create_user(self, user_data: dict) -> User:
        new_user = User(**user_data)
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user
    def get_all_users(self) -> list[User]:
        return self.db_session.query(User).filter(User.role=="student").all()