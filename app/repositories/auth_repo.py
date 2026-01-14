from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base import BaseRepository


class AuthRepository(BaseRepository["User"]):
    
    MODEL = User

    def create(self , user : User , db:Session) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_email(self , email : str , db : Session) -> User | None :
        
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt).scalar_one_or_none()
        return result
 

    def list(self , db :Session):
        stmt = select(User)
        result = db.execute(stmt).scalars().all()
        return result

    def get_by_id(self, user_id : str ,  db : Session)->User :
        stmt = select(User).where(User.id == user_id)
        result = db.execute(stmt).scalar_one_or_none()
        return result
