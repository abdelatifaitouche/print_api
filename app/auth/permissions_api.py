from fastapi import Depends, status
from app.utils.private_route import PrivateRoute
from app.auth.permission_context import PermissionContext
from app.schemas.user_schema import User
from fastapi.exceptions import HTTPException

from app.enums.permissions import Permissions
from app.schemas.jwt_payload import JwtPayload


def get_current_user(payload: JwtPayload = Depends(PrivateRoute())) -> User:
    return payload


def get_context(payload: JwtPayload = Depends(get_current_user)) -> PermissionContext:
    permission_context: PermissionContext = PermissionContext(payload)

    return permission_context


def require_permission(*permission: Permissions) -> PermissionContext:
    def permission_check(ctx: PermissionContext = Depends(get_context)):
        if not ctx.has_any_permission(*permission):
            raise HTTPException(
                detail="Not authorized", status_code=status.HTTP_401_UNAUTHORIZED
            )
        return ctx

    return permission_check
