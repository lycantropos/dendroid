from __future__ import annotations

from collections.abc import Iterable, Iterator, Set
from typing import Any, Generic

from reprit.base import generate_repr

from .abcs import AbstractSet, Tree
from .hints import Item, KeyT, ValueT
from .nil import NIL
from .utils import split_items


class BaseView(Generic[KeyT, ValueT]):
    __slots__ = ('tree',)

    def __init__(self, tree: Tree[KeyT, ValueT]) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __len__(self, /) -> int:
        return len(self.tree)


@Set.register
class ItemsView(BaseView[KeyT, ValueT], AbstractSet[Item[KeyT, ValueT]]):
    def __contains__(self, item: Item[KeyT, ValueT]) -> bool:
        key, value = item
        node = self.tree.find(key)
        return node is not NIL and node.value == value

    def __iter__(self, /) -> Iterator[Item[KeyT, ValueT]]:
        for node in self.tree:
            yield node.item

    def __reversed__(self, /) -> Iterator[Item[KeyT, ValueT]]:
        for node in reversed(self.tree):
            yield node.item

    def from_iterable(
        self, value: Iterable[Item[KeyT, ValueT]], /
    ) -> ItemsView[KeyT, ValueT]:
        keys, values = split_items(list(value))
        return ItemsView(self.tree.from_components(keys, values))


@Set.register
class KeysView(BaseView[KeyT, Any], AbstractSet[KeyT]):
    def __contains__(self, key: KeyT) -> bool:
        return self.tree.find(key) is not NIL

    def __iter__(self, /) -> Iterator[KeyT]:
        for node in self.tree:
            yield node.key

    def __reversed__(self, /) -> Iterator[KeyT]:
        for node in reversed(self.tree):
            yield node.key

    def from_iterable(self, _value: Iterable[KeyT]) -> KeysView[KeyT]:
        return KeysView(self.tree.from_components(_value))


class ValuesView(BaseView[Any, ValueT]):
    def __contains__(self, value: ValueT) -> bool:
        return any(candidate == value for candidate in self)

    def __iter__(self, /) -> Iterator[ValueT]:
        for node in self.tree:
            yield node.value

    def __reversed__(self, /) -> Iterator[ValueT]:
        for node in reversed(self.tree):
            yield node.value
