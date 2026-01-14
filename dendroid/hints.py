from typing import TypeAlias

from ._core import hints as _hints, maps as _maps, sets as _sets
from ._core.hints import KeyT as _KeyT, ValueT as _ValueT

Item: TypeAlias = _hints.Item[_KeyT, _ValueT]
Map: TypeAlias = _maps.Map[_KeyT, _ValueT]
Order: TypeAlias = _hints.Order[_ValueT, _KeyT]
KeyedSet: TypeAlias = _sets.KeyedSet[_KeyT, _ValueT]
Set: TypeAlias = _sets.Set[_ValueT]
