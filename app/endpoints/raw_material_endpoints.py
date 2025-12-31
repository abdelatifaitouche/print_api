from fastapi import APIRouter , Depends
from app.config.database import get_db
from app.services.raw_material_service import RawMaterialService
from app.schemas.raw_material_schema import RawMaterialRead , RawMaterialCreate , RawMaterialUpdate
from sqlalchemy.orm import Session
from typing import List

raw_material_endpoints = APIRouter()

raw_material_service = RawMaterialService()



@raw_material_endpoints.get("/" , response_model=List[RawMaterialRead])
def list_raw_materials(db : Session = Depends(get_db)):
    data : List[RawMaterialRead]  = raw_material_service.list(db)
    return data




@raw_material_endpoints.post("/")
def create_raw_material(data : RawMaterialCreate , db : Session = Depends(get_db))->RawMaterialRead:
    material : RawMaterialRead = raw_material_service.create(data , db)
    return material



@raw_material_endpoints.get("/{material_id}")
def get_raw_material_by_id(material_id : str , db : Session = Depends(get_db)):
    material : RawMaterialRead = raw_material_service.get_by_id(material_id , db)
    return material

@raw_material_endpoints.patch("/{material_id}/")
def update_raw_material(material_id : str , data : RawMaterialUpdate ,  db : Session = Depends(get_db)):
    material : RawMaterialRead = raw_material_service.update(material_id , data , db)
    return material




@raw_material_endpoints.delete("/{material_id}/")
def delete_raw_material(material_id : str , db : Session = Depends(get_db)):

    return raw_material_service.delete(material_id , db)

