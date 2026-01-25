from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from .jwt_utils import JwtManager
from fastapi.exceptions import HTTPException
from fastapi import status
from app.enums.permissions import Permissions
from app.enums.roles import Roles
from app.schemas.user_schema import User
from app.auth.jwt.jwt_service import JwtService
from app.schemas.jwt_payload import JwtPayload


class PrivateRoute:
    """
    Checks whether a user is authenticated via jwt manager token validity

    """

    async def __call__(self, request: Request) -> JwtPayload:
        token = request.cookies.get("access_token")

        if not token:
            raise HTTPException(
                detail="Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            payload: JwtPayload = JwtService.decode_token(token)
            return payload

        except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_401_UNAUTHORIZED)
