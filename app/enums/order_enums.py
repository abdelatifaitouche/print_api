from enum import StrEnum




class OrderStatus(StrEnum):
    PENDING = "pending" 
    PROCESSING = "processing" 
    PARTIALLY_SHIPPED = "partially_shipped" 
    SHIPPED = "shipped"       
    DELIVERED = "delivered"   
    CANCELLED = "cancelled"   
    RETURNED = "returned"     
