from fastapi import APIRouter , Depends ,Response

from app.schemas.user_schema import UserCreate , User , UserLogin
from app.services.auth_service import AuthService
from app.config.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials
from app.utils.private_route import PrivateRoute
from app.enums.roles import Roles
auth_endpoints = APIRouter()

auth_service = AuthService()


@auth_endpoints.get("/")
def index():
    return "hello from auth"




@auth_endpoints.post("/register_user/" , response_model = User)
def register_user(user_data : UserCreate , db:Session = Depends(get_db) , user:dict = Depends(PrivateRoute(roles=[Roles.ADMIN]))):
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
        max_age=36000,
        path="/"
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


#get user profile (user_data)
#get all users (only for the admin)

@auth_endpoints.get("/me" , response_model=User)
def get_user_profile(user : dict = Depends(PrivateRoute(roles=[Roles.ADMIN , Roles.USER]))):
    print(user) 
    user_profile : User = User(username = user["name"] , email=user["email"] , role=user["role"])
    
    return user_profile


@auth_endpoints.get("/users" , response_model=List[User])
def list_users(db : Session = Depends(get_db) , user : dict = Depends(PrivateRoute(roles=[Roles.ADMIN])))-> List[User]:
    users : List[User] = auth_service.get_all_users(db)
    return users



@auth_endpoints.get("/protected")
def protected_route(credentials : HTTPAuthorizationCredentials = Depends(PrivateRoute(roles=["admin" , "user"]))):
    return "testing"
