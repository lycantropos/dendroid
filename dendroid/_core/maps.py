from __future__ import annotations

import typing as _t
from collections import abc

import typing_extensions as _te
from reprit.base import generate_repr

from .abcs import (NIL,
                   Node,
                   Tree)
from .hints import (Item,
                    Key,
                    Value)
from .utils import split_items
from .views import (ItemsView,
                    KeysView,
                    ValuesView)


class Map(_t.Generic[Key, Value]):
    __slots__ = 'tree',

    def __init__(self, tree: Tree[Key, _t.Optional[Value]]) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __contains__(self, key: Key) -> bool:
        return self.tree.find(key) is not NIL

    def __copy__(self) -> Map[Key, Value]:
        return Map(self.tree.__copy__())

    def __delitem__(self, key: Key) -> None:
        node = self.tree.pop(key)
        if node is NIL:
            raise KeyError(key)

    @_t.overload
    def __eq__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __eq__(self, other: _t.Any) -> _t.Any:
        ...

    def __eq__(self, other: _t.Any) -> _t.Any:
        return (self.keys() == other.keys()
                and all(other[key] == value
                        for key, value in self.items())
                if isinstance(other, Map)
                else NotImplemented)

    def __getitem__(self, key: Key) -> _t.Optional[Value]:
        return self._find_node(key).value

    def __iter__(self) -> _t.Iterator[Key]:
        for node in self.tree:
            yield node.key

    def __len__(self) -> int:
        return len(self.tree)

    def __reversed__(self) -> _t.Iterator[Key]:
        for node in reversed(self.tree):
            yield node.key

    def __setitem__(self, key: Key, value: Value) -> None:
        self.tree.insert(key, value).value = value

    def ceil(self, key: Key) -> _t.Optional[Value]:
        return self._ceil_node(key).value

    def ceilitem(self, key: Key) -> Item[Key, _t.Optional[Value]]:
        return self._ceil_node(key).item

    def clear(self) -> None:
        self.tree.clear()

    def floor(self, key: Key) -> _t.Optional[Value]:
        return self._floor_node(key).value

    def flooritem(self, key: Key) -> Item[Key, _t.Optional[Value]]:
        return self._floor_node(key).item

    def get(self,
            key: Key,
            default: _t.Optional[Value] = None) -> _t.Optional[Value]:
        node = self.tree.find(key)
        return default if node is NIL else node.value

    def items(self) -> ItemsView[Key, _t.Optional[Value]]:
        return ItemsView(self.tree)

    def keys(self) -> KeysView[Key]:
        return KeysView(self.tree)

    def max(self) -> _t.Optional[Value]:
        return self._max_node().value

    def maxitem(self) -> Item[Key, _t.Optional[Value]]:
        return self._max_node().item

    def min(self) -> _t.Optional[Value]:
        return self._min_node().value

    def minitem(self) -> Item[Key, _t.Optional[Value]]:
        return self._min_node().item

    def next(self, key: Key) -> _t.Optional[Value]:
        return self._next_node(key).value

    def nextitem(self, key: Key) -> Item[Key, _t.Optional[Value]]:
        return self._next_node(key).item

    __sentinel = object()

    def pop(self,
            key: Key,
            default: Value = _t.cast(Value, __sentinel)) -> _t.Optional[Value]:
        node = self.tree.pop(key)
        if node is NIL:
            if default is self.__sentinel:
                raise KeyError(key)
            return default
        return node.value

    def popmax(self) -> _t.Optional[Value]:
        return self._popmax_node().value

    def popmaxitem(self) -> Item[Key, _t.Optional[Value]]:
        return self._popmax_node().item

    def popmin(self) -> _t.Optional[Value]:
        return self._popmin_node().value

    def popminitem(self) -> Item[Key, _t.Optional[Value]]:
        return self._popmin_node().item

    popitem = popminitem

    def prev(self, key: Key) -> _t.Optional[Value]:
        return self._prev_node(key).value

    def previtem(self, key: Key) -> Item[Key, _t.Optional[Value]]:
        return self._prev_node(key).item

    def setdefault(self,
                   key: Key,
                   default: _t.Optional[Value] = None) -> _t.Optional[Value]:
        node = self.tree.find(key)
        return (self.tree.insert(key, default)
                if node is NIL
                else node).value

    def update(
            self, other: _t.Union[_te.Self, _t.Iterable[Item[Key, Value]]] = ()
    ) -> None:
        items = _t.cast(_t.Iterable[Item[Key, Value]],
                        other.items() if isinstance(other, Map) else other)
        for key, value in items:
            self[key] = value

    def values(self) -> ValuesView[Key, _t.Optional[Value]]:
        return ValuesView(self.tree)

    def _ceil_node(self, key: Key) -> Node[Key, _t.Optional[Value]]:
        node = self.tree.supremum(key)
        if node is NIL:
            raise KeyError('No key found greater than or equal to {!r}'
                           .format(key))
        return node

    def _find_node(self, key: Key) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.find(key)
        if result is NIL:
            raise KeyError(key)
        return result

    def _floor_node(self, key: Key) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.infimum(key)
        if result is NIL:
            raise KeyError('No key found less than or equal to {!r}'
                           .format(key))
        return result

    def _max_node(self) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.max()
        if result is NIL:
            raise KeyError('Map is empty')
        return result

    def _min_node(self) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.min()
        if result is NIL:
            raise KeyError('Map is empty')
        return result

    def _next_node(self, key: Key) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.successor(self._find_node(key))
        if result is NIL:
            raise KeyError('Corresponds to maximum')
        return result

    def _popmax_node(self) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.popmax()
        if result is NIL:
            raise KeyError('Map is empty')
        return result

    def _popmin_node(self) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.popmin()
        if result is NIL:
            raise KeyError('Map is empty')
        return result

    def _prev_node(self, key: Key) -> Node[Key, _t.Optional[Value]]:
        result = self.tree.predecessor(self._find_node(key))
        if result is NIL:
            raise KeyError('Corresponds to minimum')
        return result


abc.MutableMapping.register(Map)


def map_constructor(
        tree_constructor: _t.Callable[
            [_t.Iterable[Key], _t.Iterable[Value]],
            Tree[Key, _t.Optional[Value]]
        ],
        *items: Item[Key, Value]
) -> Map[Key, Value]:
    return Map(tree_constructor(*split_items(items)))
