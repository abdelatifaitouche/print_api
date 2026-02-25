from abc import ABC, abstractmethod
from app.enums.order_enums import OrderStatus
from app.enums.order_items_status import OrderItemStatus
from app.models.order import OrderModel as OrderModelDb
from app.models.order_item import OrderItem as OrderItemDb
from app.execeptions.base import ValidationError

VALID_TRANSITIONS: dict[OrderItemStatus, OrderItemStatus] = {
    OrderItemStatus.PENDING: OrderItemStatus.WAIT_FOR_PROCESSING,
    OrderItemStatus.WAIT_FOR_PROCESSING: OrderItemStatus.PROCESSING,
    OrderItemStatus.PROCESSING: OrderItemStatus.PRINTED,
    OrderItemStatus.PRINTED: OrderItemStatus.DELIVERED,
    OrderItemStatus.DELIVERED: OrderItemStatus.PAIED,
    OrderItemStatus.PAIED: OrderItemStatus.FINISHED,
}


TERMINAL_STATES: tuple[OrderItemStatus] = (
    OrderItemStatus.CANCELLED,
    OrderItemStatus.FINISHED,
)

VALID_ORDER_TRANSITIONS: dict[OrderStatus, OrderStatus] = {
    OrderStatus.PENDING: OrderStatus.ACCEPTED,
    OrderStatus.ACCEPTED: OrderStatus.PROCESSING,
    OrderStatus.PROCESSING: OrderStatus.PROCESSED,
    OrderStatus.PROCESSED: OrderStatus.PARTIAL_DELIVERED,
    OrderStatus.PARTIAL_DELIVERED: OrderStatus.DELIVERED,
    OrderStatus.PARTIAL_PAIED: OrderStatus.PAIED,
    OrderStatus.PAIED: OrderStatus.FINISHED,
}


def derive_order_state(all_states: list[OrderItemStatus]) -> OrderStatus | None:
    unique = set(all_states)

    if unique == {OrderItemStatus.FINISHED}:
        return OrderStatus.FINISHED

    if unique == {OrderItemStatus.PAIED}:
        return OrderStatus.PAIED

    if OrderItemStatus.PAIED in unique:
        return OrderStatus.PARTIAL_PAIED

    if unique == {OrderItemStatus.DELIVERED}:
        return OrderStatus.DELIVERED

    if OrderItemStatus.DELIVERED in unique:
        return OrderStatus.PARTIAL_DELIVERED

    if unique == {OrderItemStatus.PRINTED}:
        return OrderStatus.PROCESSED

    if OrderItemStatus.PROCESSING in unique:
        return OrderStatus.PROCESSING
    return None


def get_valid_transition(item: OrderItemDb) -> OrderItemStatus:
    if item.status not in VALID_TRANSITIONS.keys():
        raise ValidationError(message="Invalid Transition State")

    if item.status in TERMINAL_STATES:
        raise ValidationError(message="Terminal State Reached")

    return VALID_TRANSITIONS[item.status]


def transition(item: OrderItemDb, all_items: list):
    next_state: OrderItemStatus = get_valid_transition(item)

    all_states = [next_state if i.id == item.id else i.status for i in all_items]

    print("all states : ")
    print(all_states)

    order_status = derive_order_state(all_states)

    return next_state, order_status

