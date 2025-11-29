from pydantic import BaseModel


class OrderCreate(BaseModel): 
    order_name : str
    order_price : int
