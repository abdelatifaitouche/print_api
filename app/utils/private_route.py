from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from .jwt_utils import JwtManager
from fastapi.exceptions import HTTPException
from fastapi import status
from app.enums.permissions import Permissions
from app.enums.roles import Roles

class PrivateRoute:    
    """
        Defines the Protected routes that requires the user to be authenticated,
            - checks if the token is present in the request(from HTTPONLY_COOKIES)
            - checks token validity from the jwt_manager
            - decodes the token's payload 
            - role : we 

    """       
    
    roles_permissions : dict[Roles , Permissions] = {Roles.ADMIN : Permissions.CAN_SEE_ALL , Roles.USER : Permissions.CAN_CREATE}


    def __init__(self , roles : []) : 
        self.__ROLES : list = roles

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

        if user_data["role"] not in self.__ROLES : 
            raise HTTPException(detail="UnAuthorized" , status_code = status.HTTP_401_UNAUTHORIZED)

        user_data["perms"] = self.roles_permissions[user_data["role"]]
        return user_data
