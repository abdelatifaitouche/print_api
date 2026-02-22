from abc import ABC, abstractmethod
from app.enums.order_enums import OrderStatus
from app.enums.order_items_status import OrderItemStatus
from app.models.order import OrderModel as OrderModelDb
from app.models.order_item import OrderItem as OrderItemDb


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

    if {OrderItemStatus.FINISHED.value} == unique:
        return OrderStatus.FINISHED

    if OrderItemStatus.PROCESSING.value in unique:
        return OrderStatus.PROCESSING

    if {OrderItemStatus.PRINTED.value} == unique:
        return OrderStatus.PROCESSED

    if OrderItemStatus.PAIED.value in unique:
        return OrderStatus.PARTIAL_PAIED

    if {OrderItemStatus.PAIED.value} == unique:
        return OrderStatus.PAIED
    return None


def transition(item: OrderItemDb, all_items: list):
    print("----------TRANSITION FUNCTION STARTED------------------------")
    if item.status not in VALID_TRANSITIONS.keys():
        raise ValueError("Invalid transition")

    if item.status in TERMINAL_STATES:
        raise ValueError("Cant transition in TERMINAL STATE")

    next_state = VALID_TRANSITIONS[item.status]

    print(f"NEXT ITEM STATE : {next_state}")
    all_states = []
    for i in all_items:
        if str(i.id) == str(item.id):
            print(f"appending the next state {i.id} == {item.id}")
            all_states.append(next_state)
        else:
            all_states.append(i.status)
    print(f"ALL ITEMS STATES : {all_states}")

    order_status = derive_order_state(all_states)

    print(f"NEXT ITEM STATE : {next_state} , NEXT_ORDER_STATE : {order_status}")
    print("-------------------------------------------------------------------")
    return next_state, order_status
