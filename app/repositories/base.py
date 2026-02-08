from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.base import Base
from app.execeptions.base import DatabaseError, ValidationError, AlreadyExistsError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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
            self.db.refresh(data)
            return data
        except IntegrityError as e:
            self.db.rollback()

            if "unique constraint" in str(e.orig).lower():
                raise AlreadyExistsError(
                    message=f"{self.MODEL.__name__} already exists",
                    details={"error": str(e.orig)},
                )
            elif "foreign key" in str(e.orig).lower():
                raise ValidationError(
                    message=f"Invalid Reference in {self.MODEL.__name__}",
                    details={"error": str(e.orig)},
                )

            raise DatabaseError(
                message=f"Failed to create {self.MODEL.__name__}",
                details={"error": str(e.orig)},
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(
                message=f"Failed to create {self.MODEL.__name__}",
                details={"error": str(e)},
            )

    def list(self, filters) -> list[T]:
        try:
            stmt = select(self.MODEL)

            if filters["user_id"] is not None:
                stmt = stmt.where(self.MODEL.created_by == filters["user_id"])

            stmt = stmt.order_by(self.MODEL.created_at.desc()).limit(10).offset(0)

            result = self.db.execute(stmt).scalars().all()

            return result
        except SQLAlchemyError as e:
            raise DatabaseError(
                message=f"Failed to fetch {self.MODEL.__name__} list",
                details={"error": str(e)},
            )

    def get_by_id(self, entity_id: str) -> T:
        try:
            stmt = select(self.MODEL).where(self.MODEL.id == entity_id)
            result = self.db.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError(
                message=f"Failed to fetch {self.MODEL.__name__}",
                details={"entity_id": entity_id, "error": str(e)},
            )
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
            entity = self.db.get(self.MODEL, entity_id)

            if entity:
                self.db.delete(entity)
                self.db.commit()
                return True
            else:
                return False
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(
                message=f"Cannot delete {self.MODEL.__name__}",
                details={
                    "entity_id": entity_id,
                    "error": str(e.orig),
                },
            )

        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(
                message=f"Failed to delete {self.MODEL.__name__}",
                details={
                    "entity_id": entity_id,
                    "error": str(e),
                },
            )
