from app.config.database import BASE
import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped , mapped_column


class Base(BASE):
    """
    base model to use for all our data

    """

    __abstract__ = True

    id : Mapped[str] = mapped_column(primary_key=True , default=lambda:str(uuid.uuid4()),index=True , unique=True) 
    created_at : Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at : Mapped[datetime] = mapped_column(default=datetime.utcnow() , onupdate=datetime.utcnow())
