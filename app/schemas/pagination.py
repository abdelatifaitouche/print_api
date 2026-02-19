from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    total_pages: int = 0
    total_items: int = 0
    model_config = {"from_attributes": True}
