from __future__ import annotations

from collections import abc
from typing import Any

from reprit.base import generate_repr
from typing_extensions import Self, override

from .abcs import AbstractSet, Collection, HasRepr, Tree
from .hints import Item, KeyT, ValueT
from .nil import NIL
from .utils import split_items


class ItemsView(HasRepr, AbstractSet[Item[KeyT, ValueT]]):
    @override
    def from_iterable(
        self, value: abc.Iterable[Item[KeyT, ValueT]], /
    ) -> Self:
        keys, values = split_items(list(value))
        return type(self)(self._tree.from_components(keys, values))

    __slots__ = ('_tree',)

    @override
    def __contains__(self, item: Item[KeyT, ValueT], /) -> bool:
        key, value = item
        node = self._tree.find(key)
        return node is not NIL and node.value == value

    def __init__(self, _tree: Tree[KeyT, ValueT], /) -> None:
        self._tree = _tree

    @override
    def __iter__(self, /) -> abc.Iterator[Item[KeyT, ValueT]]:
        for node in self._tree:
            yield node.item

    @override
    def __len__(self, /) -> int:
        return len(self._tree)

    __repr__ = generate_repr(__init__)

    def __reversed__(self, /) -> abc.Iterator[Item[KeyT, ValueT]]:
        for node in reversed(self._tree):
            yield node.item


class KeysView(HasRepr, AbstractSet[KeyT]):
    @override
    def from_iterable(self, _value: abc.Iterable[KeyT], /) -> KeysView[KeyT]:
        return KeysView(self._tree.from_components(_value))

    __slots__ = ('_tree',)

    @override
    def __contains__(self, key: KeyT, /) -> bool:
        return self._tree.find(key) is not NIL

    def __init__(self, _tree: Tree[KeyT, Any], /) -> None:
        self._tree = _tree

    @override
    def __iter__(self, /) -> abc.Iterator[KeyT]:
        for node in self._tree:
            yield node.key

    @override
    def __len__(self, /) -> int:
        return len(self._tree)

    __repr__ = generate_repr(__init__)

    def __reversed__(self, /) -> abc.Iterator[KeyT]:
        for node in reversed(self._tree):
            yield node.key


abc.Set.register(ItemsView)  # pyright: ignore[reportAttributeAccessIssue]
abc.Set.register(KeysView)  # pyright: ignore[reportAttributeAccessIssue]


class ValuesView(HasRepr, Collection[ValueT]):
    __slots__ = ('_tree',)

    @override
    def __contains__(self, value: ValueT, /) -> bool:
        return any(candidate == value for candidate in self)

    def __init__(self, _tree: Tree[KeyT, ValueT], /) -> None:
        self._tree = _tree

    @override
    def __iter__(self, /) -> abc.Iterator[ValueT]:
        for node in self._tree:
            yield node.value

    @override
    def __len__(self, /) -> int:
        return len(self._tree)

    __repr__ = generate_repr(__init__)

    def __reversed__(self, /) -> abc.Iterator[ValueT]:
        for node in reversed(self._tree):
            yield node.value


abc.Collection.register(  # pyright: ignore[reportAttributeAccessIssue]
    ItemsView
)
