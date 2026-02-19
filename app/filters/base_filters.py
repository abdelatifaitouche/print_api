from .interface import IFilters
from sqlalchemy import Select


class BaseFilters(IFilters):
    def __init__(self, user_id: str | None = None, status: str | None = None):
        self.status: str | None = status
        self.user_id: str | None = user_id

    def apply(self, stmt: Select, model):
        if self.user_id:
            stmt = stmt.where(model.created_by == self.user_id)

        if self.status:
            stmt = stmt.where(model.status == self.status)

        return stmt
