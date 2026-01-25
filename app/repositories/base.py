from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    MODEL: Type[T] | None = None  # type: ignore

    def __init__(self):
        if self.MODEL is None:
            raise TypeError(f"{self.__class__.__name__} must set MODEL")

    def create(self, data: T, db: Session) -> T:
        try:
            db.add(data)
            db.commit()
            db.flush()
            return data
        except Exception as e:
            db.rollback()
            raise e

    def list(self, filters, db: Session) -> list[T]:
        stmt = select(self.MODEL)

        if filters["user_id"] is not None:
            stmt = stmt.where(self.MODEL.created_by == filters["user_id"])

        stmt = stmt.order_by(self.MODEL.created_at.desc()).limit(10).offset(0)

        result = db.execute(stmt).scalars().all()

        return result

    def get_by_id(self, entity_id: str, db: Session) -> T:
        stmt = select(self.MODEL).where(self.MODEL.id == entity_id)
        result = db.execute(stmt).scalar_one_or_none()

        return result

    def update(self, entity: T, data: dict, db: Session) -> T:
        try:
            for field, value in data.items():
                setattr(entity, field, value)

            db.commit()
            db.refresh(entity)
            return entity
        except Exception as e:
            db.rollback()
            raise e

    def delete(self, entity_id: str, db: Session) -> bool:
        try:
            stmt = delete(self.MODEL).where(self.MODEL.id == entity_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
