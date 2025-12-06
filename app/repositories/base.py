from typing import Type , TypeVar , Generic


T = TypeVar("T")


class BaseRepository(Generic[T]):
    model : Type[T]


