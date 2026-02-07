from app.repositories.raw_material_repo import RawMaterialRepository
from app.schemas.raw_material_schema import (
    RawMaterialRead,
    RawMaterialCreate,
    RawMaterialUpdate,
)
from app.models.raw_material import RawMaterial as RawMaterialDb

from sqlalchemy.orm import Session

from app.services.base_service import BaseService


class RawMaterialService(
    BaseService[RawMaterialDb, RawMaterialCreate, RawMaterialRead, RawMaterialUpdate]
):
    READ_SCHEMA = RawMaterialRead
    CREATE_SCHEMA = RawMaterialCreate
    UPDATE_SCHEMA = RawMaterialUpdate
    DB_MODEL = RawMaterialDb

    REPO_CLASS = RawMaterialRepository
