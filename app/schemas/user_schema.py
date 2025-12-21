from pydantic import BaseModel
from app.enums.roles import Roles


class UserCreate(BaseModel):
    username : str
    email : str
    password : str
    role : Roles
    model_config = {"from_attributes" : True}

class User(BaseModel):
    username : str
    email : str
    role : Roles | None = None
    model_config ={"from_attributes" : True}


class UserLogin(BaseModel):
    email : str
    password: str
