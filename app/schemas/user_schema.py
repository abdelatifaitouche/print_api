from pydantic import BaseModel
from app.enums.roles import Roles


class CompanyBase(BaseModel):
    id: str
    name: str
    email: str
    address: str
    phone: str
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Roles
    company_id: str | None = None
    model_config = {"from_attributes": True}


class User(BaseModel):
    id: str
    username: str
    email: str
    role: Roles | None = None
    company: CompanyBase | None = None
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: str
    password: str


class UserAdminUpdate(BaseModel):
    email: str | None = None
    role: str | None = None
    company_id: str | None = None
    username: str | None = None


class UserContext(BaseModel):
    id: str
    role: Roles
    company_id: str
