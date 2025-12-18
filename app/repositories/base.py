from typing import Type , TypeVar , Generic , List
from sqlalchemy.orm import Session
from sqlalchemy import select , delete

T = TypeVar("T")


class BaseRepository(Generic[T]):
    MODEL : Type[T]

    
    def create(self , data : T ,  db : Session)->T:
        try : 
            db.add(data)
            db.commit()
            db.flush()
            return data
        except Exception as e : 
            db.rollback()
            raise e

    def list(self ,db :Session) -> List[T]:
        stmt = select(self.MODEL)
        result = db.execute(stmt).scalars().all()

        return result

    
    def get_by_id(self , entity_id : str , db:Session) -> T : 
        
        stmt = select(self.MODEL).where(self.MODEL.id == entity_id)
        result = db.execute(stmt).scalar_one_or_none()

        return result


    def update(self , entity : T , data : dict ,  db : Session) -> T:
        
        try : 
            for field, value in data.items():
                setattr(entity , field ,value)

            db.commit()
            db.refresh(entity)
            return entity
        except Exception as e : 
            db.rollback()
            raise e

    def delete(self , entity_id : str , db :Session) -> bool : 
        stmt = delete(self.MODEL).where(self.MODEL.id == entity_id)
        result = db.execute(stmt)
        db.commit()
        
        return result.rowcount > 0
