from app.models.user import User
from app.schemas.user import  UserResponse
from sqlalchemy.orm import joinedload


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def findById(self, id: int) -> User:
        return self.db_session.query(User).filter(User.id == id).options(
            joinedload(User.addresses)
        )




