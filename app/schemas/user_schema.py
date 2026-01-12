from pydantic import BaseModel
from app.enums.roles import Roles

class UserCreate(BaseModel):
    username : str
    email : str
    password : str
    role : Roles
    company_id : str | None = None
    model_config = {"from_attributes" : True}

class User(BaseModel):
    id : str
    username : str
    email : str
    role : Roles | None = None
    company_id : str | None = None
    model_config ={"from_attributes" : True}


class UserLogin(BaseModel):
    email : str
    password: str
