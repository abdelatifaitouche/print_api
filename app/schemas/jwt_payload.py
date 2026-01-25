from pydantic import BaseModel
from uuid import UUID
from app.enums.roles import Roles
from datetime import datetime


class JwtPayload(BaseModel):
    user_id: UUID
    company_id: UUID
    email: str
    role: Roles
    username: str
    iat: datetime | None = None
    exp: datetime | None = None

    class Config:
        json_encoders = {datetime: lambda v: int(v.timestamp())}
