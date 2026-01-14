from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Iterable, Iterator
from typing import Any, Generic

from reprit.base import generate_repr

from .abcs import MutableSet, Tree
from .hints import KeyT, Order, ValueT
from .nil import NIL


class BaseSet(MutableSet[ValueT]):
    __slots__ = ('tree',)

    def __init__(self, tree: Tree[Any, ValueT]) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __iter__(self, /) -> Iterator[ValueT]:
        for node in self.tree:
            yield node.value

    def __len__(self, /) -> int:
        return len(self.tree)

    def __reversed__(self, /) -> Iterator[ValueT]:
        for node in reversed(self.tree):
            yield node.value

    @abstractmethod
    def ceil(self, value: ValueT) -> ValueT:
        """Returns first value not less than the given one."""

    def clear(self, /) -> None:
        self.tree.clear()

    @abstractmethod
    def floor(self, value: ValueT) -> ValueT:
        """Returns first value not greater than the given one."""

    def max(self, /) -> ValueT:
        node = self.tree.max()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    def min(self, /) -> ValueT:
        node = self.tree.min()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    @abstractmethod
    def next(self, value: ValueT) -> ValueT:
        """Returns first value greater than the given one."""

    def popmax(self, /) -> ValueT:
        node = self.tree.popmax()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    def popmin(self, /) -> ValueT:
        node = self.tree.popmin()
        if node is NIL:
            raise ValueError('Set is empty')
        return node.value

    pop = popmin

    @abstractmethod
    def prev(self, value: ValueT) -> ValueT:
        """Returns last value lesser than the given one."""


class Set(BaseSet[ValueT]):
    def __contains__(self, value: ValueT, /) -> bool:
        return self.tree.find(value) is not NIL

    def __copy__(self, /) -> Set[ValueT]:
        return Set(self.tree.__copy__())

    def add(self, value: ValueT, /) -> None:
        self.tree.insert(value, value)

    def ceil(self, value: ValueT, /) -> ValueT:
        node = self.tree.supremum(value)
        if node is NIL:
            raise ValueError(
                f'No value found greater than or equal to {value!r}'
            )
        return node.value

    def discard(self, value: ValueT, /) -> None:
        node = self.tree.find(value)
        if node is NIL:
            return
        self.tree.remove(node)

    def floor(self, value: ValueT, /) -> ValueT:
        node = self.tree.infimum(value)
        if node is NIL:
            raise ValueError(f'No value found less than or equal to {value!r}')
        return node.value

    def from_iterable(self, _value: Iterable[KeyT], /) -> Set[KeyT]:
        return Set(self.tree.from_components(_value))

    def next(self, value: ValueT, /) -> ValueT:
        node = self.tree.find(value)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self.tree.successor(node)
        if node is NIL:
            raise ValueError('Corresponds to maximum')
        return node.value

    def prev(self, value: ValueT, /) -> ValueT:
        node = self.tree.find(value)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self.tree.predecessor(node)
        if node is NIL:
            raise ValueError('Corresponds to minimum')
        return node.value

    def remove(self, value: ValueT, /) -> None:
        node = self.tree.pop(value)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')


class KeyedSet(Generic[KeyT, ValueT], BaseSet[ValueT]):
    __slots__ = ('key',)

    def __init__(
        self, tree: Tree[KeyT, ValueT], key: Order[ValueT, KeyT]
    ) -> None:
        super().__init__(tree)
        self.key = key

    __repr__ = generate_repr(__init__)

    def __contains__(self, value: ValueT, /) -> bool:
        return bool(self.tree) and self.tree.find(self.key(value)) is not NIL

    def __copy__(self, /) -> KeyedSet[KeyT, ValueT]:
        return KeyedSet(self.tree.__copy__(), self.key)

    def add(self, value: ValueT, /) -> None:
        self.tree.insert(self.key(value), value)

    def ceil(self, value: ValueT, /) -> ValueT:
        node = self.tree.supremum(self.key(value))
        if node is NIL:
            raise ValueError(
                f'No value found greater than or equal to {value!r}'
            )
        return node.value

    def discard(self, value: ValueT, /) -> None:
        node = self.tree.find(self.key(value))
        if node is NIL:
            return
        self.tree.remove(node)

    def floor(self, value: ValueT, /) -> ValueT:
        node = self.tree.infimum(self.key(value))
        if node is NIL:
            raise ValueError(f'No value found less than or equal to {value!r}')
        return node.value

    def from_iterable(
        self, _value: Iterable[ValueT], /
    ) -> KeyedSet[KeyT, ValueT]:
        values = list(_value)
        return KeyedSet(
            self.tree.from_components(map(self.key, values), values), self.key
        )

    def next(self, value: ValueT, /) -> ValueT:
        key = self.key(value)
        node = self.tree.find(key)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self.tree.successor(node)
        if node is NIL:
            raise ValueError('Corresponds to maximum')
        return node.value

    def prev(self, value: ValueT, /) -> ValueT:
        key = self.key(value)
        node = self.tree.find(key)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self.tree.predecessor(node)
        if node is NIL:
            raise ValueError('Corresponds to minimum')
        return node.value

    def remove(self, value: ValueT, /) -> None:
        node = self.tree.pop(self.key(value))
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')


def set_constructor(
    tree_constructor: Callable[..., Tree[KeyT, ValueT]],
    /,
    *values: ValueT,
    key: Order[ValueT, KeyT] | None = None,
) -> BaseSet[ValueT]:
    return (
        Set(tree_constructor(values))
        if key is None
        else KeyedSet(
            tree_constructor([key(value) for value in values], values), key
        )
    )
