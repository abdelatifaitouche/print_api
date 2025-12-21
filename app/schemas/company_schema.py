
from pydantic import BaseModel
from app.enums.company_enums import FolderStatus
from typing import Optional
from datetime import datetime
from uuid import UUID

class CompanyRead(BaseModel):
    id : UUID
    name : str
    address : str
    email : str
    phone : str
    folder_status : FolderStatus | None = FolderStatus.PENDING
    drive_folder_id : str | None = None
    created_at : datetime 
    created_by : UUID
    model_config = {'from_attributes' : True}

class CompanyCreate(BaseModel):
    name : str
    address : str
    email : str
    phone : str
    created_by : str|None = None

    model_config = {'from_attributes' : True}


class CompanyUpdate(BaseModel):
    name : Optional[str] = None
    address : Optional[str] = None
    email : Optional[str] = None
    phone : Optional[str] = None
    folder_status : Optional[FolderStatus] = None


