from typing import (Callable,
                    TypeVar)

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

Domain = TypeVar('Domain')
OtherDomain = TypeVar('OtherDomain')


class Sortable(Protocol):
    def __lt__(self, other: 'Sortable') -> bool:
        """Checks if the object is less than given one."""


SortingKey = Callable[[Domain], Sortable]
