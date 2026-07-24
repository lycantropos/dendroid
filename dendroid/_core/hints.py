from collections.abc import Callable
from typing import Any, Protocol, Self, TypeAlias, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


KeyT = TypeVar('KeyT', bound=Ordered)
ValueT = TypeVar('ValueT', bound=Any)
Order: TypeAlias = Callable[[ValueT], KeyT]
Item: TypeAlias = tuple[KeyT, ValueT]
