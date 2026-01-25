from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from app.schemas.user_schema import (
    UserCreate,
    User,
    UserLogin,
    UserAdminUpdate,
    UserContext,
)
from app.services.auth_service import AuthService
from app.config.database import get_db
from sqlalchemy.orm import Session

from app.utils.private_route import PrivateRoute
from app.enums.roles import Roles
from typing import List
from app.auth.permission_context import PermissionContext
from app.auth.permissions_api import require_permission
from app.enums.permissions import Permissions
from app.schemas.jwt_payload import JwtPayload

auth_endpoints = APIRouter()

auth_service = AuthService()


@auth_endpoints.get("/")
def index():
    return "hello from auth"


@auth_endpoints.post("/register_user/", response_model=User)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_CREATE_ALL),
    ),
):
    user = auth_service.create(user_data, db)
    return user


@auth_endpoints.post("/login/")
def login_user(
    login_data: UserLogin, response: Response, db: Session = Depends(get_db)
):
    access_token = auth_service.login_user(login_data, db)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=36000,
        path="/",
    )
    return "logged in"


@auth_endpoints.post("/logout/")
def logout_user(response: Response):
    response.set_cookie(
        key="access_token", value="", httponly=True, secure=False, samesite="lax"
    )
    return "loggedout"


# get user profile (user_data)
# get all users (only for the admin)


@auth_endpoints.get(
    "/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK
)
def get_user_by_id(
    user_id: str, db: Session = Depends(get_db), user: dict = Depends(PrivateRoute())
):
    user: User = auth_service.get_user_by_id(user_id, db)

    return user


@auth_endpoints.get("/me", status_code=status.HTTP_200_OK)
def get_user_profile(payload: JwtPayload | None = Depends(PrivateRoute())):
    return payload


@auth_endpoints.get("/users", response_model=List[User])
def list_users(
    db: Session = Depends(get_db),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_READ_ALL)),
) -> List[User]:
    users: List[User] = auth_service.list(db=db)
    return users


@auth_endpoints.patch(
    "/users/{user_id}/", response_model=User, status_code=status.HTTP_200_OK
)
def admin_update_user(
    user_id: str,
    data: UserAdminUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(PrivateRoute()),
):
    user: User = auth_service.update(user_id, data, db)
    return user
