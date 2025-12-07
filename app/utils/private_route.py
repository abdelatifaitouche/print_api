from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from .jwt_utils import JwtManager
from fastapi.exceptions import HTTPException
from fastapi import status
class PrivateRoute(HTTPBearer):
    
    
    async def __call__(self , request : Request) -> HTTPAuthorizationCredentials:
        creds =  await super().__call__(request)

        print(f"creds from my private route {creds.credentials}")


        """
            we are getting the creds here,
            we need to do a validity check
        """

        
        token_validity : bool = JwtManager().verify_token(creds.credentials)
        
        if not token_validity : 
            raise HTTPException(detail="UnAuthorized" , status = status.HTTP_401_UNAUTHORIZED)
