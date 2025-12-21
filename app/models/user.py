from sqlalchemy.orm import Mapped , mapped_column 
from sqlalchemy import String , Integer
from .base import Base
from app.enums.roles import Roles


class User(Base):
    __tablename__="users"

    username : Mapped[str] = mapped_column(String , nullable=False)
    email : Mapped[str] = mapped_column(String , nullable=False , unique=True)
    password : Mapped[str] = mapped_column(String , nullable=False)
    role : Mapped[str] = mapped_column(String , server_default = Roles.USER)
