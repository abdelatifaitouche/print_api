from .base_filters import BaseFilters
from sqlalchemy import Select


class OrderFilters(BaseFilters):
    def __init__(
        self,
        all: bool = False,
        user_id: str | None = None,
        status: str | None = None,
        company_id: str | None = None,
    ):
        self.company_id = company_id
        super().__init__(all, user_id, status)

    def apply(self, stmt: Select, model):
        stmt = super().apply(stmt, model)

        if self.company_id:
            stmt = stmt.where(model.company_id == self.company_id)

        return stmt
