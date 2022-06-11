from typing import Optional, Tuple, TypeVar

from typing_extensions import (Protocol,
                               TypeAlias)

from .core import (hints as _hints,
                   maps as _maps,
                   sets as _sets)

Key: TypeAlias = _hints.Key
Value: TypeAlias = _hints.Value
Item = _hints.Item
Order = _hints.Order
Map = _maps.Map
Set = _sets.Set

_Key = TypeVar('_Key',
               bound=_hints.Ordered)
_Value = TypeVar('_Value')


class MapFactory(Protocol[_Key, _Value]):
    def __call__(self, *items: Tuple[_Key, _Value]) -> Map[_Key, _Value]:
        ...


_T = TypeVar('_T')


class SetFactory(Protocol[_T]):
    def __call__(self,
                 *values: _T,
                 key: Optional[_hints.Order] = None) -> _sets.BaseSet[_T]:
        ...
