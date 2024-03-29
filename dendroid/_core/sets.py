from __future__ import annotations

import typing as _t
from abc import abstractmethod

from reprit.base import generate_repr

from .abcs import (NIL,
                   MutableSet,
                   Tree)
from .hints import (Key,
                    Order,
                    Value)


class BaseSet(MutableSet[Value]):
    __slots__ = 'tree',

    def __init__(self, tree: Tree[_t.Any, Value]) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __iter__(self) -> _t.Iterator[Value]:
        for node in self.tree:
            yield node.value

    def __len__(self) -> int:
        return len(self.tree)

    def __reversed__(self) -> _t.Iterator[Value]:
        for node in reversed(self.tree):
            yield node.value

    @abstractmethod
    def ceil(self, value: Value) -> Value:
        """Returns first value not less than the given one."""

    def clear(self) -> None:
        self.tree.clear()

    @abstractmethod
    def floor(self, value: Value) -> Value:
        """Returns first value not greater than the given one."""

    def max(self) -> Value:
        node = self.tree.max()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    def min(self) -> Value:
        node = self.tree.min()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    @abstractmethod
    def next(self, value: Value) -> Value:
        """Returns first value greater than the given one."""

    def popmax(self) -> Value:
        node = self.tree.popmax()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    def popmin(self) -> Value:
        node = self.tree.popmin()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    pop = popmin

    @abstractmethod
    def prev(self, value: Value) -> Value:
        """Returns last value lesser than the given one."""


class Set(BaseSet[Value]):
    def __contains__(self, value: Value) -> bool:
        return self.tree.find(value) is not NIL

    def __copy__(self) -> Set[Value]:
        return Set(self.tree.__copy__())

    def add(self, value: Value) -> None:
        self.tree.insert(value, value)

    def ceil(self, value: Value) -> Value:
        node = self.tree.supremum(value)
        if node is NIL:
            raise ValueError('No value found greater than or equal to {!r}'
                             .format(value))
        return node.value

    def discard(self, value: Value) -> None:
        node = self.tree.find(value)
        if node is NIL:
            return
        self.tree.remove(node)

    def floor(self, value: Value) -> Value:
        node = self.tree.infimum(value)
        if node is NIL:
            raise ValueError('No value found less than or equal to {!r}'
                             .format(value))
        return node.value

    def from_iterable(self, _value: _t.Iterable[Key]) -> Set[Key]:
        return Set(self.tree.from_components(_value))

    def next(self, value: Value) -> Value:
        node = self.tree.find(value)
        if node is NIL:
            raise ValueError('{!r} is not in set'.format(value))
        node = self.tree.successor(node)
        if node is NIL:
            raise ValueError('Corresponds to maximum')
        return node.value

    def prev(self, value: Value) -> Value:
        node = self.tree.find(value)
        if node is NIL:
            raise ValueError('{!r} is not in set'.format(value))
        node = self.tree.predecessor(node)
        if node is NIL:
            raise ValueError('Corresponds to minimum')
        return node.value

    def remove(self, value: Value) -> None:
        node = self.tree.pop(value)
        if node is NIL:
            raise ValueError('{!r} is not in set'.format(value))


class KeyedSet(_t.Generic[Key, Value], BaseSet[Value]):
    __slots__ = 'key',

    def __init__(self, tree: Tree[Key, Value], key: Order[Value, Key]) -> None:
        super().__init__(tree)
        self.key = key

    __repr__ = generate_repr(__init__)

    def __contains__(self, value: Value) -> bool:
        return bool(self.tree) and self.tree.find(self.key(value)) is not NIL

    def __copy__(self) -> KeyedSet[Key, Value]:
        return KeyedSet(self.tree.__copy__(), self.key)

    def add(self, value: Value) -> None:
        self.tree.insert(self.key(value), value)

    def ceil(self, value: Value) -> Value:
        node = self.tree.supremum(self.key(value))
        if node is NIL:
            raise ValueError('No value found greater than or equal to {!r}'
                             .format(value))
        return node.value

    def discard(self, value: Value) -> None:
        node = self.tree.find(self.key(value))
        if node is NIL:
            return
        self.tree.remove(node)

    def floor(self, value: Value) -> Value:
        node = self.tree.infimum(self.key(value))
        if node is NIL:
            raise ValueError('No value found less than or equal to {!r}'
                             .format(value))
        return node.value

    def from_iterable(self,
                      _value: _t.Iterable[Value]) -> KeyedSet[Key, Value]:
        values = list(_value)
        return KeyedSet(self.tree.from_components(map(self.key, values),
                                                  values),
                        self.key)

    def next(self, value: Value) -> Value:
        key = self.key(value)
        node = self.tree.find(key)
        if node is NIL:
            raise ValueError('{!r} is not in set'.format(value))
        node = self.tree.successor(node)
        if node is NIL:
            raise ValueError('Corresponds to maximum')
        return node.value

    def prev(self, value: Value) -> Value:
        key = self.key(value)
        node = self.tree.find(key)
        if node is NIL:
            raise ValueError('{!r} is not in set'.format(value))
        node = self.tree.predecessor(node)
        if node is NIL:
            raise ValueError('Corresponds to minimum')
        return node.value

    def remove(self, value: Value) -> None:
        node = self.tree.pop(self.key(value))
        if node is NIL:
            raise ValueError('{!r} is not in set'.format(value))


def set_constructor(
        tree_constructor: _t.Callable[..., Tree[Key, Value]],
        *values: Value,
        key: _t.Optional[Order[Value, Key]] = None
) -> BaseSet[Value]:
    return (Set(tree_constructor(values))
            if key is None
            else KeyedSet(tree_constructor([key(value) for value in values],
                                           values),
                          key))
