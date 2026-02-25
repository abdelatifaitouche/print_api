from pydantic import BaseModel
from app.enums.company_enums import FolderStatus
from typing import Optional
from datetime import datetime
from uuid import UUID
from typing import List
from app.schemas.user_schema import User


class CompanySummary(BaseModel):
    id: str
    name: str
    email: str
    phone: str

    model_config = {"from_attributes": True}


class CompanyBase(BaseModel):
    id: UUID
    name: str


class CompanyRead(BaseModel):
    id: UUID
    name: str
    address: str
    email: str
    phone: str
    users: List[User] | None = None
    folder_status: FolderStatus | None = FolderStatus.PENDING
    drive_folder_id: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


class CompanyCreate(BaseModel):
    name: str
    address: str
    email: str
    phone: str

    model_config = {"from_attributes": True}


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    folder_status: Optional[FolderStatus] = None
