
from app.repositories.raw_material_repo import RawMaterialRepository
from app.schemas.raw_material_schema import RawMaterialRead , RawMaterialCreate , RawMaterialUpdate
from app.models.raw_material import RawMaterial as RawMaterialDb

from sqlalchemy.orm import Session

from app.services.base_service import BaseService

class RawMaterialService(BaseService[RawMaterialDb , RawMaterialCreate,RawMaterialRead , RawMaterialUpdate]):
    
    READ_SCHEMA = RawMaterialRead
    CREATE_SCHEMA = RawMaterialCreate
    UPDATE_SCHEMA = RawMaterialUpdate
    DB_MODEL = RawMaterialDb
    
    repo = RawMaterialRepository

    def create(self , data : RawMaterialCreate , db : Session)->RawMaterialRead:
        
        if not data.name : 
            raise Exception("raw material name must be included")

        if not data.stock_quantity or data.stock_quantity <= 0 : 
            raise Exception("Invalid data for stock quantity")

        if not data.cost_per_unit or data.cost_per_unit <= 0 : 
            raise Exception("Invalid data for cost per unit")
        
        
        created_model = super().create(data , db)
    
        return created_model



