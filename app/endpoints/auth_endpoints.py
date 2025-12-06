from fastapi import APIRouter , Depends , Header
from app.schemas.user_schema import UserCreate , User , UserLogin
from app.services.auth_service import AuthService
from app.config.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials


auth_endpoints = APIRouter()

auth_service = AuthService()


@auth_endpoints.get("/")
def index():
    return "hello from auth"




@auth_endpoints.post("/register_user" , response_model = User)
def register_user(user_data : UserCreate , db:Session = Depends(get_db)):
    user = auth_service.create_user(user_data , db)
    return user



@auth_endpoints.post("/login")
def login_user(login_data : UserLogin , db : Session = Depends(get_db)):
    access_token = auth_service.login_user(login_data , db) 
    return access_token


bearer_scheme = HTTPBearer()

@auth_endpoints.get("/protected")
def protected_route(credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    print(f"getting the token from the protectected route {token}")
    return token
