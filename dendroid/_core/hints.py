from collections.abc import Callable
from typing import Any, TypeAlias, TypeVar

from typing_extensions import Protocol, Self


class Ordered(Protocol):
    def __le__(self, other: Self, /) -> bool: ...
    def __lt__(self, other: Self, /) -> bool: ...


KeyT = TypeVar('KeyT', bound=Ordered)
KeyT_co = TypeVar('KeyT_co', bound=Ordered, covariant=True)
ValueT = TypeVar('ValueT', bound=Any)
Order: TypeAlias = Callable[[ValueT], KeyT]
Item: TypeAlias = tuple[KeyT, ValueT]
