import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from app.schemas.jwt_payload import JwtPayload

load_dotenv()


class JwtService:
    """
    Service for handling jwt token ops :
        - Token generation (refresh , access)
        - Token verification
        - get user from the token
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE: int = 2  # access token expire time in hours
    REFRESH_TOKEN_EXPIRE: int = 7  # refresh token expire time in days!

    @classmethod
    def generate_access_token(cls, payload: JwtPayload) -> str:
        """
        Instead of passing a user schema
        create a payloadSchema
        """
        payload.exp = datetime.now(timezone.utc) + timedelta(
            hours=cls.ACCESS_TOKEN_EXPIRE
        )
        payload.iat = datetime.now(timezone.utc)

        token: str = jwt.encode(
            payload.model_dump(mode="json"), cls.SECRET_KEY, algorithm="HS256"
        )

        return token

    @classmethod
    def decode_token(cls, token: str) -> JwtPayload:
        try:
            decoded_token: JwtPayload = jwt.decode(
                token,
                cls.SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_signature": True, "verify_exp": True},
            )

            payload: JwtPayload = JwtPayload(
                user_id=decoded_token["user_id"],
                role=decoded_token["role"],
                email=decoded_token["email"],
                company_id=decoded_token["company_id"],
                username=decoded_token["username"],
                exp=decoded_token["exp"],
                iat=decoded_token["iat"],
            )

            return payload
        except jwt.ExpiredSignatureError as e:
            print(e)
            raise
        except jwt.InvalidSignatureError as e:
            print(e)
            raise
        except jwt.DecodeError as e:
            print(e)
            raise

    def verify_token():
        return

    def get_current_user():
        return
