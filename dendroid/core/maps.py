from collections import abc
from typing import (Callable,
                    Generic,
                    Iterable,
                    Iterator,
                    Optional,
                    Union)

from reprit.base import generate_repr

from dendroid.hints import (Item,
                            Key,
                            Value)
from .abcs import (NIL,
                   Node,
                   Tree)
from .utils import split_items
from .views import (ItemsView,
                    KeysView,
                    ValuesView)


@abc.MutableMapping.register
class Map(Generic[Key, Value]):
    __slots__ = 'tree',

    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __contains__(self, key: Key) -> bool:
        return self.tree.find(key) is not NIL

    def __copy__(self) -> 'Map[Key, Value]':
        return Map(self.tree.__copy__())

    def __delitem__(self, key: Key) -> None:
        node = self.tree.pop(key)
        if node is NIL:
            raise KeyError(key)

    def __eq__(self, other: 'Map[Key, Value]') -> bool:
        return (self.keys() == other.keys()
                and all(other[key] == value
                        for key, value in self.items())
                if isinstance(other, Map)
                else NotImplemented)

    def __getitem__(self, key: Key) -> Value:
        node = self.tree.find(key)
        if node is NIL:
            raise KeyError(key)
        return node.value

    def __iter__(self) -> Iterator[Key]:
        for node in self.tree:
            yield node.key

    def __len__(self) -> int:
        return len(self.tree)

    def __reversed__(self) -> Iterator[Key]:
        for node in reversed(self.tree):
            yield node.key

    def __setitem__(self, key: Key, value: Value) -> None:
        self.tree.insert(key, value).value = value

    def ceil(self, key: Key) -> Value:
        node = self.tree.supremum(key)
        if node is NIL:
            raise KeyError('No key found greater than or equal to {!r}'
                           .format(key))
        return node.value

    def ceilitem(self, key: Key) -> Value:
        node = self.tree.supremum(key)
        if node is NIL:
            raise KeyError('No key found greater than or equal to {!r}'
                           .format(key))
        return node.item

    def clear(self) -> None:
        self.tree.clear()

    def floor(self, key: Key) -> Value:
        node = self.tree.infimum(key)
        if node is NIL:
            raise KeyError('No key found less than or equal to {!r}'
                           .format(key))
        return node.value

    def flooritem(self, key: Key) -> Value:
        node = self.tree.infimum(key)
        if node is NIL:
            raise KeyError('No key found less than or equal to {!r}'
                           .format(key))
        return node.item

    def get(self,
            key: Key,
            default: Optional[Value] = None) -> Optional[Value]:
        node = self.tree.find(key)
        return default if node is NIL else node.value

    def items(self) -> ItemsView[Key, Value]:
        return ItemsView(self.tree)

    def keys(self) -> KeysView[Key]:
        return KeysView(self.tree)

    def max(self) -> Value:
        return self._max_node().value

    def maxitem(self) -> Value:
        return self._max_node().item

    def min(self) -> Value:
        return self._min_node().value

    def minitem(self) -> Item:
        return self._min_node().item

    def next(self, key: Key) -> Value:
        return self._next_node(key).value

    def nextitem(self, key: Key) -> Value:
        return self._next_node(key).item

    __sentinel = object()

    def pop(self, key: Key, default: Value = __sentinel) -> Value:
        node = self.tree.pop(key)
        if node is NIL:
            if default is self.__sentinel:
                raise KeyError(key)
            return default
        return node.value

    def popmax(self) -> Value:
        return self._popmax_node().value

    def popmaxitem(self) -> Value:
        return self._popmax_node().item

    def popmin(self) -> Value:
        return self._popmin_node().value

    def popminitem(self) -> Item:
        return self._popmin_node().item

    popitem = popminitem

    def prev(self, key: Key) -> Value:
        return self._prev_node(key).value

    def previtem(self, key: Key) -> Value:
        return self._prev_node(key).item

    def setdefault(self,
                   key: Key,
                   default: Optional[Value] = None) -> Optional[Value]:
        node = self.tree.find(key)
        return (self.tree.insert(key, default)
                if node is NIL
                else node).value

    def update(self,
               other: Union['Map[Key, Value]', Iterable[Item]] = ()) -> None:
        for key, value in (other.items() if isinstance(other, Map) else other):
            self[key] = value

    def values(self) -> ValuesView[Value]:
        return ValuesView(self.tree)

    def _max_node(self) -> Node:
        node = self.tree.max()
        if node is NIL:
            raise KeyError('Map is empty')
        return node

    def _min_node(self) -> Node:
        node = self.tree.min()
        if node is NIL:
            raise KeyError('Map is empty')
        return node

    def _next_node(self, key: Key) -> Node:
        node = self.tree.find(key)
        if node is NIL:
            raise KeyError(key)
        node = self.tree.successor(node)
        if node is NIL:
            raise KeyError('Corresponds to maximum')
        return node

    def _popmax_node(self) -> Node:
        node = self.tree.popmax()
        if node is NIL:
            raise KeyError('Map is empty')
        return node

    def _popmin_node(self) -> Node:
        node = self.tree.popmin()
        if node is NIL:
            raise KeyError('Map is empty')
        return node

    def _prev_node(self, key: Key) -> Node:
        node = self.tree.find(key)
        if node is NIL:
            raise KeyError(key)
        node = self.tree.predecessor(node)
        if node is NIL:
            raise KeyError('Corresponds to minimum')
        return node


def map_constructor(tree_constructor
                    : Callable[[Iterable[Key], Iterable[Value]], Tree],
                    *items: Item) -> Map[Key, Value]:
    return Map(tree_constructor(*split_items(items)))
