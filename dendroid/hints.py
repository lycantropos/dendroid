from typing import (Callable,
                    Tuple,
                    TypeVar)

Key = TypeVar('Key')
Value = TypeVar('Value')
SortingKey = Callable[[Value], Key]
Item = Tuple[Key, Value]
