from typing import Generic, List, TypeVar
from app.repositories.base import BaseRepository
from pydantic import BaseModel
from sqlalchemy.orm import Session
from abc import ABC
from app.execeptions.base import NoDataError
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

        if not data:
            raise NoDataError(
                service=self.__class__.__name__, message="No Records found"
            )

        return [self.READ_SCHEMA.from_orm(item) for item in data]

    def create(self, data: TCreateSchema) -> TReadSchema:
        if not data:
            raise NoDataError(
                serivce=self.__class__.__name__, message="No Data in the service"
            )
        data: TModel = self.repo.create(self.DB_MODEL(**data.dict()))

        return self.READ_SCHEMA.from_orm(data)

    def get_by_id(self, data_id: str) -> TReadSchema:
        if not data_id:
            raise NoDataError(service=self.__class__.__name__, message="No Data")
        data: TModel = self.repo.get_by_id(data_id)

        if data is None:
            raise NoDataError(service=self.__class__.__name__, message="No Data Found")

        return self.READ_SCHEMA.from_orm(data)

    def update(self, data_id: str, data: TUpdateSchema) -> TReadSchema:
        model: TModel = self.repo.get_by_id(data_id)

        if model is None:
            raise NoDataError(service=self.__class__.__name__, message="No Data found")

        updated_model: TModel = self.repo.update(model, (data.dict(exclude_unset=True)))

        return self.READ_SCHEMA.from_orm(updated_model)

    def delete(self, data_id: str) -> bool:
        model: TModel = self.repo.get_by_id(data_id)

        if not model:
            raise NoDataError(service=self.__class__.__name__, message="No Data Found")

        return self.repo.delete(model.id)
