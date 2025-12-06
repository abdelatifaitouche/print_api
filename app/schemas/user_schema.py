from pydantic import BaseModel



class UserCreate(BaseModel):
    username : str
    email : str
    password : str

    model_config = {"from_attributes" : True}

class User(BaseModel):
    username : str
    email : str

    model_config ={"from_attributes" : True}


class UserLogin(BaseModel):
    email : str
    password: str
