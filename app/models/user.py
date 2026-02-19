from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from .base import Base
from app.enums.roles import Roles


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, server_default=Roles.USER)

    created_orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="creator", foreign_keys="OrderModel.created_by"
    )
    company_id: Mapped[str] = mapped_column(
        String, ForeignKey("companies.id"), nullable=True
    )
    company: Mapped["CompanyModel"] = relationship(back_populates="users")
