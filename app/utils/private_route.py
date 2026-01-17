from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from .jwt_utils import JwtManager
from fastapi.exceptions import HTTPException
from fastapi import status
from app.enums.permissions import Permissions
from app.enums.roles import Roles
from app.auth.role_perms_map import ROLE_PERMISSION

class PrivateRoute:    
    """
        Checks whether a user is authenticated via jwt manager token validity
            
    """        
    async def __call__(self , request : Request):   
        token = request.cookies.get("access_token")
        
        if not token : 
            raise HTTPException(
                detail="Not authenticated",
                status_code = status.HTTP_401_UNAUTHORIZED
            )

        token_validity : bool = JwtManager().verify_token(token)
        
        if not token_validity : 
            raise HTTPException(detail="UnValid token" , status_code = status.HTTP_401_UNAUTHORIZED)
        

        user_data :  dict = JwtManager().get_user_from_token(token)
        
        if not user_data : 
            raise HTTPException(detail="Cannot get token data" , status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user_data
