from fastapi import APIRouter , Depends ,Response

from app.schemas.user_schema import UserCreate , User , UserLogin
from app.services.auth_service import AuthService
from app.config.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials
from app.utils.private_route import PrivateRoute

auth_endpoints = APIRouter()

auth_service = AuthService()


@auth_endpoints.get("/")
def index():
    return "hello from auth"




@auth_endpoints.post("/register_user/" , response_model = User)
def register_user(user_data : UserCreate , db:Session = Depends(get_db)):
    user = auth_service.create_user(user_data , db)
    return user



@auth_endpoints.post("/login/")
def login_user(login_data : UserLogin ,response:Response, db : Session = Depends(get_db)):
    access_token = auth_service.login_user(login_data , db) 
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=36000
    )
    return 'logged in'


@auth_endpoints.post('/logout/')
def logout_user(response:Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return "loggedout"

@auth_endpoints.get("/protected")
def protected_route(credentials : HTTPAuthorizationCredentials = Depends(PrivateRoute(roles=["admin" , "user"]))):
    return "testing"
