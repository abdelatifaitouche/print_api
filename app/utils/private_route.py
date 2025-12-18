from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from .jwt_utils import JwtManager
from fastapi.exceptions import HTTPException
from fastapi import status


class PrivateRoute:
    
    
    async def __call__(self , request : Request):
        
        token = request.cookies.get("access_token")
        
        if not token : 
            raise HTTPException(
                detail="Not authenticated",
                status_code = status.HTTP_401_UNAUTHORIZED
            )

        print(f"creds from my private route {token}")


        """
            we are getting the creds here,
            we need to do a validity check
        """

        
        token_validity : bool = JwtManager().verify_token(token)
        
        if not token_validity : 
            raise HTTPException(detail="UnAuthorized" , status = status.HTTP_401_UNAUTHORIZED)

        return token
