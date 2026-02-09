from enum import StrEnum


class OrderItemStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PRINTED = "printed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
