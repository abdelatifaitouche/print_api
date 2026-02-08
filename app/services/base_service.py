from typing import Generic, List, TypeVar
from app.repositories.base import BaseRepository
from pydantic import BaseModel
from sqlalchemy.orm import Session
from abc import ABC
from app.execeptions.base import NotFoundError
from app.auth.permission_context import PermissionContext

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TReadSchema = TypeVar("TReadSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)
TModel = TypeVar("TModel")


class BaseService(ABC, Generic[TModel, TCreateSchema, TReadSchema, TUpdateSchema]):
    REPO_CLASS: type[BaseRepository[TModel]]
    READ_SCHEMA: type[TReadSchema]
    CREATE_SCHEMA: type[TCreateSchema]
    UPDATE_SCHEMA: type[TUpdateSchema]
    DB_MODEL: type[TModel]

    def __init__(self, db: Session):
        self.db = db
        self.repo = self.REPO_CLASS(db)

    def list(self, user_id: str | None = None) -> list[TReadSchema]:
        filters = {}

        if user_id:
            filters["user_id"] = user_id
        else:
            filters["user_id"] = None
        data: list[TModel] = self.repo.list(filters)

        return [self.READ_SCHEMA.from_orm(item) for item in data]

    def create(self, data: TCreateSchema) -> TReadSchema:
        data: TModel = self.repo.create(self.DB_MODEL(**data.dict()))

        return self.READ_SCHEMA.from_orm(data)

    def get_by_id(self, data_id: str) -> TReadSchema:
        data: TModel = self.repo.get_by_id(data_id)

        if not data:
            raise NotFoundError(
                message=f"{self.repo.MODEL.__name__} not found",
                details={"entity_id": data_id},
            )

        return self.READ_SCHEMA.from_orm(data)

    def update(self, data_id: str, data: TUpdateSchema) -> TReadSchema:
        model: TModel = self.get_by_id(data_id)

        updated_model: TModel = self.repo.update(model, (data.dict(exclude_unset=True)))

        return self.READ_SCHEMA.from_orm(updated_model)

    def delete(self, data_id: str) -> bool:
        deleted = self.repo.delete(data_id)

        if not deleted:
            raise NotFoundError(
                message=f"{self.repo.MODEL.__name__} not found",
                details={"entity_id": data_id},
            )

        return True
