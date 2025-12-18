from enum import StrEnum



class OrderItemStatus(StrEnum):
    PENDING = "pending" 
    PROCESSING = "processing"  
    SHIPPED = "shipped"     
    DELIVERED = "delivered"    
    CANCELLED = "cancelled"    
