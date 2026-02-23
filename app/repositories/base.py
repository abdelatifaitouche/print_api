from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, func, Select
from app.models.base import Base
from app.execeptions.base import DatabaseError, ValidationError, AlreadyExistsError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.schemas.pagination import Pagination
import math
from app.filters.base_filters import BaseFilters

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

    def __apply_pagination(self, stmt: Select, pagination: Pagination | None = None):
        page_size: int = 10
        count_stmt = select(func.count()).select_from(stmt.subquery())

        total_items = self.db.scalar(count_stmt)

        total_pages: int = math.ceil(total_items / page_size)

        if not pagination:
            pagination: Pagination = Pagination(
                page=1, total_items=total_items, total_pages=total_pages
            )
        else:
            if pagination.page <= 0 or pagination.page > total_pages:
                return []
            pagination.total_items = total_items
            pagination.total_pages = total_pages

        stmt = stmt.limit(page_size).offset((pagination.page - 1) * page_size)

        return stmt, pagination

    def list(
        self,
        filters: BaseFilters | None = None,
        stmt: Select | None = None,
        pagination: Pagination | None = None,
    ) -> list[T]:
        try:
            if stmt is None:
                stmt: Select = select(self.MODEL)

            if filters:
                stmt = filters.apply(stmt, self.MODEL)

            stmt = stmt.order_by(self.MODEL.created_at.desc())

            if not filters.all:
                stmt, pagination = self.__apply_pagination(stmt, pagination)

            result: list[T] = self.db.execute(stmt).scalars().all()

            return result, pagination
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
