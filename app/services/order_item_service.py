from sqlalchemy.orm import Session

from app.models.order_item import OrderItem as OrderItemDb
from app.repositories.order_item_repo import OrderItemRepository
from app.schemas.order_item_schema import (
    OrderItemCreate,
    OrderItemRead,
    OrderItemUpdate,
)
from app.services.interface import ServiceInterface
from app.services.base_service import BaseService


class OrderItemService(
    BaseService[OrderItemDb, OrderItemCreate, OrderItemRead, OrderItemUpdate]
):
    READ_SCHEMA = OrderItemRead
    CREATE_SCHEMA = OrderItemCreate
    DB_MODEL = OrderItemDb
    UPDATE_SCHEMA = OrderItemUpdate
    REPO_CLASS = OrderItemRepository

    def create(self, order_item_data: OrderItemCreate, db: Session) -> OrderItemRead:
        order_db: OrderItemDb = OrderItemDb(**order_item_data.dict())

        order = self.__order_item_repo.create(order_db, db)

        return OrderItemRead.from_orm(order)
