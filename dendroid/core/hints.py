from typing import (Any,
                    Callable,
                    Tuple,
                    TypeVar)

from typing_extensions import Protocol

_T = TypeVar('_T',
             contravariant=True)


class Ordered(Protocol[_T]):
    def __lt__(self: _T, other: _T) -> bool:
        ...


Key = TypeVar('Key',
              bound=Ordered)
Value = TypeVar('Value',
                bound=Any)
Order = Callable[[Value], Key]
Item = Tuple[Key, Value]
