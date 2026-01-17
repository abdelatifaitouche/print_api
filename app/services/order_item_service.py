from sqlalchemy.orm import Session

from app.models.order_item import OrderItem as OrderItemDb
from app.repositories.order_item_repo import OrderItemRepository
from app.schemas.order_item_schema import OrderItemCreate, OrderItemRead
from app.services.interface import ServiceInterface


class OrderItemService(ServiceInterface):
    def __init__(self):
        self.__order_item_repo = OrderItemRepository()

    def list(self):
        pass

    def create(self, order_item_data: OrderItemCreate, db: Session) -> OrderItemRead:
        order_db: OrderItemDb = OrderItemDb(**order_item_data.dict())

        order = self.__order_item_repo.create(order_db, db)

        return OrderItemRead.from_orm(order)

    def get_by_id(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
