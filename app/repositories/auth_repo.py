from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base import BaseRepository


class AuthRepository(BaseRepository["User"]):
    MODEL = User

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result
