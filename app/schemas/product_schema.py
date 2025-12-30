from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List 
from .raw_material_schema import RawMaterialRead

class ProductMaterialCreate(BaseModel):
    raw_material_id : str
    quantity :Decimal

class ProductMaterialRead(ProductMaterialCreate):
    pass

class ProductRead(BaseModel):
    id : str
    name : str
    description : str
    base_price : float | None = None
    created_at : datetime
    updated_at : datetime 
    raw_materials : List[RawMaterialRead] 

    model_config = {"from_attributes" : True}


class ProductCreate(BaseModel):
    name : str
    base_price : float
    description : str
    raw_materials : List[ProductMaterialCreate]


class ProductLightRead(BaseModel):
    id : str
    name : str
    description : str
    base_price : float | None = None
    
    model_config = {"from_attributes" : True}


class ProductUpdate(ProductCreate):
    pass

