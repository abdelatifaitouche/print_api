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
from app.enums.order_items_status import OrderItemStatus

from app.repositories.order_repo import OrderRepository
from app.workflows.state_engine import transition


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

    def pay_item(self, item_id: str):
        item: OrderItemDb = self.repo.get_by_id(item_id)

        paied_item = super().update(
            item_id, OrderItemUpdate(status=OrderItemStatus.PAIED)
        )
        return paied_item

    def transition(self, item_id: str):
        print("TRIGGERING THE TRANSITION SERVICE")
        from app.services.order_service import OrderService
        from app.schemas.order_schema import OrderRead, OrderUpdate

        print(f"Getting the item with id {item_id}")
        item: OrderItemDb = self.repo.get_by_id(item_id)
        order_service = OrderService(self.db)

        print(f"Getting the order with id : {item.order_id} ")
        order: OrderRead = order_service.get_by_id(item.order_id)
        next_item_state, next_order_state = transition(item, order.items)

        if next_order_state is not None:
            print(f"Updating the order states to  : {next_order_state}")
            order_service.update(item.order_id, OrderUpdate(status=next_order_state))

        print(f"transitioning the item state to {next_item_state}")

        transitioned_item: OrderItemRead = super().update(
            item_id, OrderItemUpdate(status=next_item_state)
        )

        return transitioned_item
