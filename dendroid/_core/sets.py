from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable, Iterator
from typing import Any, Generic

from reprit.base import generate_repr
from typing_extensions import Self, override

from .abcs import HasRepr, MutableSet, Tree, TreeWrapper
from .hints import KeyT, Order, ValueT
from .nil import NIL


class BaseSet(TreeWrapper[Any, ValueT], MutableSet[ValueT]):
    @abstractmethod
    def ceil(self, value: ValueT, /) -> ValueT:
        """Returns first value not less than the given one."""

    def clear(self, /) -> None:
        self.tree.clear()

    @abstractmethod
    def floor(self, value: ValueT, /) -> ValueT:
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
    def next(self, value: ValueT, /) -> ValueT:
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
    def prev(self, value: ValueT, /) -> ValueT:
        """Returns last value lesser than the given one."""

    __slots__ = ()

    def __iter__(self, /) -> Iterator[ValueT]:
        for node in self.tree:
            yield node.value

    def __len__(self, /) -> int:
        return len(self.tree)

    def __reversed__(self, /) -> Iterator[ValueT]:
        for node in reversed(self.tree):
            yield node.value


class Set(HasRepr, BaseSet[ValueT]):
    @property
    @override
    def tree(self, /) -> Tree[Any, ValueT]:
        return self._tree

    @override
    def add(self, value: ValueT, /) -> None:
        self._tree.insert(value, value)

    @override
    def ceil(self, value: ValueT, /) -> ValueT:
        node = self._tree.supremum(value)
        if node is NIL:
            raise ValueError(
                f'No value found greater than or equal to {value!r}'
            )
        return node.value

    @override
    def discard(self, value: ValueT, /) -> None:
        node = self._tree.find(value)
        if node is NIL:
            return
        self._tree.remove(node)

    @override
    def floor(self, value: ValueT, /) -> ValueT:
        node = self._tree.infimum(value)
        if node is NIL:
            raise ValueError(f'No value found less than or equal to {value!r}')
        return node.value

    @override
    def from_iterable(self, value: Iterable[KeyT], /) -> Set[KeyT]:
        return Set(self._tree.from_components(value))

    @override
    def next(self, value: ValueT, /) -> ValueT:
        node = self._tree.find(value)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self._tree.successor(node)
        if node is NIL:
            raise ValueError('Corresponds to maximum')
        return node.value

    @override
    def prev(self, value: ValueT, /) -> ValueT:
        node = self._tree.find(value)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self._tree.predecessor(node)
        if node is NIL:
            raise ValueError('Corresponds to minimum')
        return node.value

    @override
    def remove(self, value: ValueT, /) -> None:
        node = self._tree.pop(value)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')

    __slots__ = ('_tree',)

    def __contains__(self, value: ValueT, /) -> bool:
        return self._tree.find(value) is not NIL

    def __copy__(self, /) -> Self:
        return type(self)(self._tree.__copy__())

    def __init__(self, tree: Tree[Any, ValueT], /) -> None:
        self._tree = tree

    __repr__ = generate_repr(__init__)


class KeyedSet(HasRepr, Generic[KeyT, ValueT], BaseSet[ValueT]):
    @property
    def key(self, /) -> Order[ValueT, KeyT]:
        return self._key

    @property
    @override
    def tree(self, /) -> Tree[KeyT, ValueT]:
        return self._tree

    def add(self, value: ValueT, /) -> None:
        self._tree.insert(self._key(value), value)

    def ceil(self, value: ValueT, /) -> ValueT:
        node = self._tree.supremum(self._key(value))
        if node is NIL:
            raise ValueError(
                f'No value found greater than or equal to {value!r}'
            )
        return node.value

    def discard(self, value: ValueT, /) -> None:
        node = self._tree.find(self._key(value))
        if node is NIL:
            return
        self._tree.remove(node)

    def floor(self, value: ValueT, /) -> ValueT:
        node = self._tree.infimum(self._key(value))
        if node is NIL:
            raise ValueError(f'No value found less than or equal to {value!r}')
        return node.value

    def from_iterable(
        self, _value: Iterable[ValueT], /
    ) -> KeyedSet[KeyT, ValueT]:
        values = list(_value)
        return KeyedSet(
            self._tree.from_components(map(self._key, values), values),
            self._key,
        )

    def next(self, value: ValueT, /) -> ValueT:
        key = self._key(value)
        node = self._tree.find(key)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self._tree.successor(node)
        if node is NIL:
            raise ValueError('Corresponds to maximum')
        return node.value

    def prev(self, value: ValueT, /) -> ValueT:
        key = self._key(value)
        node = self._tree.find(key)
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')
        node = self._tree.predecessor(node)
        if node is NIL:
            raise ValueError('Corresponds to minimum')
        return node.value

    def remove(self, value: ValueT, /) -> None:
        node = self._tree.pop(self._key(value))
        if node is NIL:
            raise ValueError(f'{value!r} is not in set')

    __slots__ = '_key', '_tree'

    def __contains__(self, value: ValueT, /) -> bool:
        return (
            bool(self._tree) and self._tree.find(self._key(value)) is not NIL
        )

    def __copy__(self, /) -> Self:
        return type(self)(self._tree.__copy__(), self._key)

    def __init__(
        self, tree: Tree[KeyT, ValueT], key: Order[ValueT, KeyT], /
    ) -> None:
        self._key, self._tree = key, tree

    __repr__ = generate_repr(__init__)
