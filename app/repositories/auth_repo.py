from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select



class AuthRepository:


    def create(self , user : User , db:Session) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_email(self , email : str , db : Session) -> User | None :
        
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt).scalar_one_or_none()
        return result
 

    def list():
        return

    def get_by_id():
        return
