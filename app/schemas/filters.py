from pydantic import BaseModel
from app.enums.order_enums import OrderStatus


class Filters(BaseModel):
    user_id: str | None = None
    company_id: str | None = None
    status: OrderStatus | None = None
