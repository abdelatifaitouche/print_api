from enum import StrEnum


class OrderItemStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WAIT_FOR_PROCESSING = "WAIT_FOR_PROCESSING:"
    PROCESSING = "processing"
    PRINTED = "printed"
    SHIPPED = "shipped"
    DELIVERED = "delivred"
    CANCELLED = "cancelled"
