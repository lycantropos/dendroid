from typing import (Optional as _Optional,
                    Tuple as _Tuple,
                    TypeVar as _TypeVar)

from typing_extensions import Protocol as _Protocol

from .core import (hints as _hints,
                   maps as _maps,
                   sets as _sets)
from .core.hints import (Key,
                         Value)

Item = _hints.Item
Map = _maps.Map
Order = _hints.Order
Set = _sets.Set


class MapFactory(_Protocol[Key, Value]):
    def __call__(self, *items: Item) -> Map[Key, Value]:
        ...


class SetFactory(_Protocol[Value]):
    def __call__(self,
                 *values: Value,
                 key: _Optional[Order] = None) -> _sets.BaseSet[Value]:
        ...
