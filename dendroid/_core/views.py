from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Generic, override

from reprit.base import generate_repr

from .abcs import AbstractSet, HasRepr, Tree, TreeWrapper
from .hints import Item, KeyT, ValueT
from .nil import NIL
from .utils import split_items


class ItemsView(
    HasRepr, TreeWrapper[KeyT, ValueT], AbstractSet[Item[KeyT, ValueT]]
):
    @property
    @override
    def tree(self, /) -> Tree[KeyT, ValueT]:
        return self._tree

    def from_iterable(
        self, value: Iterable[Item[KeyT, ValueT]], /
    ) -> ItemsView[KeyT, ValueT]:
        keys, values = split_items(list(value))
        return ItemsView(self._tree.from_components(keys, values))

    def __contains__(self, item: Item[KeyT, ValueT], /) -> bool:
        key, value = item
        node = self._tree.find(key)
        return node is not NIL and node.value == value

    def __init__(self, _tree: Tree[KeyT, ValueT], /) -> None:
        self._tree = _tree

    def __iter__(self, /) -> Iterator[Item[KeyT, ValueT]]:
        for node in self._tree:
            yield node.item

    def __len__(self, /) -> int:
        return len(self._tree)

    __repr__ = generate_repr(__init__)

    def __reversed__(self, /) -> Iterator[Item[KeyT, ValueT]]:
        for node in reversed(self._tree):
            yield node.item


class KeysView(HasRepr, TreeWrapper[KeyT, Any], AbstractSet[KeyT]):
    @property
    @override
    def tree(self, /) -> Tree[KeyT, Any]:
        return self._tree

    def __contains__(self, key: KeyT, /) -> bool:
        return self._tree.find(key) is not NIL

    def __init__(self, tree: Tree[KeyT, Any], /) -> None:
        self._tree = tree

    def __iter__(self, /) -> Iterator[KeyT]:
        for node in self._tree:
            yield node.key

    def __len__(self, /) -> int:
        return len(self._tree)

    __repr__ = generate_repr(__init__)

    def __reversed__(self, /) -> Iterator[KeyT]:
        for node in reversed(self._tree):
            yield node.key

    def from_iterable(self, _value: Iterable[KeyT], /) -> KeysView[KeyT]:
        return KeysView(self._tree.from_components(_value))


class ValuesView(HasRepr, Generic[ValueT]):
    def __contains__(self, value: ValueT, /) -> bool:
        return any(candidate == value for candidate in self)

    def __init__(self, tree: Tree[KeyT, ValueT], /) -> None:
        self._tree = tree

    def __iter__(self, /) -> Iterator[ValueT]:
        for node in self._tree:
            yield node.value

    def __len__(self, /) -> int:
        return len(self._tree)

    __repr__ = generate_repr(__init__)

    def __reversed__(self, /) -> Iterator[ValueT]:
        for node in reversed(self._tree):
            yield node.value
