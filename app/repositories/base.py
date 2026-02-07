from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    MODEL: Type[T] | None = None  # type: ignore

    def __init__(self, db: Session):
        self.db = db
        if self.MODEL is None:
            raise TypeError(f"{self.__class__.__name__} must set MODEL")

    def create(self, data: T) -> T:
        try:
            self.db.add(data)
            self.db.commit()
            return data
        except Exception as e:
            self.db.rollback()
            raise e

    def list(self, filters) -> list[T]:
        stmt = select(self.MODEL)

        if filters["user_id"] is not None:
            stmt = stmt.where(self.MODEL.created_by == filters["user_id"])

        stmt = stmt.order_by(self.MODEL.created_at.desc()).limit(10).offset(0)

        result = self.db.execute(stmt).scalars().all()

        return result

    def get_by_id(self, entity_id: str) -> T:
        stmt = select(self.MODEL).where(self.MODEL.id == entity_id)
        result = self.db.execute(stmt).scalar_one_or_none()

        return result

    def update(self, entity: T, data: dict) -> T:
        try:
            for field, value in data.items():
                setattr(entity, field, value)

            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, entity_id: str) -> bool:
        try:
            stmt = delete(self.MODEL).where(self.MODEL.id == entity_id)
            result = self.db.execute(stmt)
            self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            self.db.rollback()
            raise e
