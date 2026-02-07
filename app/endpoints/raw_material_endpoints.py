from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.services.raw_material_service import RawMaterialService
from app.schemas.raw_material_schema import (
    RawMaterialRead,
    RawMaterialCreate,
    RawMaterialUpdate,
)
from sqlalchemy.orm import Session
from typing import List
from app.auth.permission_context import PermissionContext
from app.auth.permissions_api import require_permission
from app.enums.permissions import Permissions

raw_material_endpoints = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return RawMaterialService(db)


@raw_material_endpoints.get("/", response_model=List[RawMaterialRead])
def list_raw_materials(
    raw_material_service: RawMaterialService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_READ_ALL),
    ),
):
    data: List[RawMaterialRead] = raw_material_service.list()
    return data


@raw_material_endpoints.post("/")
def create_raw_material(
    data: RawMaterialCreate,
    raw_material_service: RawMaterialService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_CREATE_ALL),
    ),
) -> RawMaterialRead:
    material: RawMaterialRead = raw_material_service.create(data)
    return material


@raw_material_endpoints.get("/{material_id}")
def get_raw_material_by_id(
    material_id: str, raw_material_service: RawMaterialService = Depends(get_service)
):
    material: RawMaterialRead = raw_material_service.get_by_id(material_id)
    return material


@raw_material_endpoints.patch("/{material_id}/")
def update_raw_material(
    material_id: str,
    data: RawMaterialUpdate,
    raw_material_service: RawMaterialService = Depends(get_service),
):
    material: RawMaterialRead = raw_material_service.update(material_id, data)
    return material


@raw_material_endpoints.delete("/{material_id}/")
def delete_raw_material(
    material_id: str, raw_material_service: RawMaterialService = Depends(get_service)
):
    return raw_material_service.delete(material_id)
