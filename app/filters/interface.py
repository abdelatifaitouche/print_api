from abc import ABC, abstractmethod
from sqlalchemy import Select


class IFilters(ABC):
    @abstractmethod
    def apply(self, stmt: Select):
        pass
