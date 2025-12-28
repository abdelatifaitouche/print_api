from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class RawMaterialRead(BaseModel):
    id : str
    name : str
    stock_quantity : Decimal
    cost_per_unit : Decimal
    created_at : datetime
    updated_at : datetime
    model_config = {"from_attributes" : True}


class RawMaterialCreate(BaseModel):
    name : str
    stock_quantity : Decimal
    cost_per_unit : Decimal


class RawMaterialUpdate(BaseModel):
    name : str | None = None
    stock_quantity : Decimal|None = None
    cost_per_unit : Decimal|None = None
