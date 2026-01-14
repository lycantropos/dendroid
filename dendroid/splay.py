from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import cast, overload

from typing_extensions import Self, override

from ._core import abcs as _abcs, nil as _nil
from ._core.hints import (
    Item as _Item,
    KeyT as _KeyT,
    Order as _Order,
    ValueT as _ValueT,
)
from ._core.maps import Map as _Map
from ._core.sets import KeyedSet as _KeyedSet, Set as _Set
from ._core.utils import (
    split_items as _split_items,
    to_unique_sorted_items as _to_unique_sorted_items,
    to_unique_sorted_values as _to_unique_sorted_values,
)
from .binary import Node as Node

NIL = _nil.NIL
Nil = _nil.Nil


class Tree(_abcs.Tree[_KeyT, _ValueT]):
    @overload
    @classmethod
    def from_components(
        cls: type[Tree[_KeyT, _KeyT]],
        _keys: Iterable[_KeyT],
        _values: None = ...,
    ) -> Tree[_KeyT, _KeyT]: ...

    @overload
    @classmethod
    def from_components(
        cls, _keys: Iterable[_KeyT], _values: Iterable[_ValueT]
    ) -> Self: ...

    @classmethod
    def from_components(
        cls: type[Tree[_KeyT, _KeyT]] | type[Tree[_KeyT, _ValueT]],
        _keys: Iterable[_KeyT],
        _values: Iterable[_ValueT] | None = None,
    ) -> Tree[_KeyT, _KeyT] | Tree[_KeyT, _ValueT]:
        keys = list(_keys)
        if not keys:
            return cls(NIL)
        if _values is None:
            keys = _to_unique_sorted_values(keys)

            def to_simple_node(
                start_index: int, end_index: int
            ) -> Node[_KeyT, _KeyT]:
                middle_index = (start_index + end_index) // 2
                key = keys[middle_index]
                return Node(
                    key,
                    key,
                    left=(
                        to_simple_node(start_index, middle_index)
                        if middle_index > start_index
                        else NIL
                    ),
                    right=(
                        to_simple_node(middle_index + 1, end_index)
                        if middle_index < end_index - 1
                        else NIL
                    ),
                )

            return cast(type[Tree[_KeyT, _KeyT]], cls)(
                to_simple_node(0, len(keys))
            )
        items = _to_unique_sorted_items(keys, tuple(_values))

        def to_complex_node(
            start_index: int, end_index: int, /
        ) -> Node[_KeyT, _ValueT]:
            middle_index = (start_index + end_index) // 2
            key, value = items[middle_index]
            return Node(
                key,
                value,
                left=(
                    to_complex_node(start_index, middle_index)
                    if middle_index > start_index
                    else NIL
                ),
                right=(
                    to_complex_node(middle_index + 1, end_index)
                    if middle_index < end_index - 1
                    else NIL
                ),
            )

        return cast(type[Tree[_KeyT, _ValueT]], cls)(
            to_complex_node(0, len(items))
        )

    @property
    @override
    def root(self, /) -> Node[_KeyT, _ValueT] | Nil:
        return self._root

    @override
    def find(self, key: _KeyT, /) -> Node[_KeyT, _ValueT] | Nil:
        if self._root is NIL:
            return NIL
        self._splay(key)
        root = self._root
        return NIL if key < root.key or root.key < key else root

    @override
    def insert(self, key: _KeyT, value: _ValueT, /) -> Node[_KeyT, _ValueT]:
        if self._root is NIL:
            node = self._root = Node(key, value)
            return node
        self._splay(key)
        if key < self._root.key:
            self._root.left, self._root = (
                NIL,
                Node(key, value, left=self._root.left, right=self._root),
            )
        elif self._root.key < key:
            self._root.right, self._root = (
                NIL,
                Node(key, value, left=self._root, right=self._root.right),
            )
        return self._root

    @override
    def max(self, /) -> Node[_KeyT, _ValueT] | Nil:
        node = self._root
        if node is not NIL:
            while node.right is not NIL:
                node = node.right
            self._splay(node.key)
        return node

    @override
    def min(self, /) -> Node[_KeyT, _ValueT] | Nil:
        node = self._root
        if node is not NIL:
            while node.left is not NIL:
                node = node.left
            self._splay(node.key)
        return node

    @override
    def popmax(self, /) -> Node[_KeyT, _ValueT] | Nil:
        if self._root is NIL:
            return self._root
        result = self.max()
        self._remove_root()
        return result

    @override
    def popmin(self, /) -> Node[_KeyT, _ValueT] | Nil:
        if self._root is NIL:
            return self._root
        result = self.min()
        self._remove_root()
        return result

    @override
    def predecessor(
        self, node: _abcs.Node[_KeyT, _ValueT], /
    ) -> Node[_KeyT, _ValueT] | Nil:
        result: Node[_KeyT, _ValueT] | Nil
        assert isinstance(node, Node), node
        if node.left is not NIL:
            result = node.left
            while result.right is not NIL:
                result = result.right
        else:
            result, cursor, key = NIL, self._root, node.key
            while cursor is not node:
                assert cursor is not NIL
                if cursor.key < key:
                    result, cursor = cursor, cursor.right
                else:
                    cursor = cursor.left
        if result is not NIL:
            self._splay(result.key)
        return result

    @override
    def remove(self, node: _abcs.Node[_KeyT, _ValueT], /) -> None:
        assert isinstance(node, Node), node
        self._splay(node.key)
        self._remove_root()

    @override
    def successor(
        self, node: _abcs.Node[_KeyT, _ValueT], /
    ) -> Node[_KeyT, _ValueT] | Nil:
        assert isinstance(node, Node), node
        result: Node[_KeyT, _ValueT] | Nil
        if node.right is not NIL:
            result = node.right
            while result.left is not NIL:
                result = result.left
        else:
            result, cursor, key = NIL, self._root, node.key
            while cursor is not node:
                assert cursor is not NIL
                if key < cursor.key:
                    result, cursor = cursor, cursor.left
                else:
                    cursor = cursor.right
        if result is not NIL:
            self._splay(result.key)
        return result

    @staticmethod
    def _rotate_left(node: Node[_KeyT, _ValueT], /) -> Node[_KeyT, _ValueT]:
        replacement = node.right
        assert replacement is not NIL
        node.right, replacement.left = replacement.left, node
        return replacement

    @staticmethod
    def _rotate_right(node: Node[_KeyT, _ValueT], /) -> Node[_KeyT, _ValueT]:
        replacement = node.left
        assert replacement is not NIL
        node.left, replacement.right = replacement.right, node
        return replacement

    def _remove_root(self, /) -> None:
        root = self._root
        assert root is not NIL
        if root.left is NIL:
            self._root = root.right
        else:
            right_root_child = root.right
            self._root = root.left
            self._splay(root.key)
            self._root.right = right_root_child

    def _splay(self, key: _KeyT, /) -> None:
        next_root = self._root
        next_root_left_child = next_root_right_child = self._header
        while True:
            assert next_root is not NIL
            if key < next_root.key:
                if next_root.left is NIL:
                    break
                if key < next_root.left.key:
                    next_root = self._rotate_right(next_root)
                    if next_root.left is NIL:
                        break
                next_root_right_child.left = next_root
                next_root_right_child, next_root = next_root, next_root.left
            elif next_root.key < key:
                if next_root.right is NIL:
                    break
                if next_root.right.key < key:
                    next_root = self._rotate_left(next_root)
                    if next_root.right is NIL:
                        break
                next_root_left_child.right = next_root
                next_root_left_child, next_root = next_root, next_root.right
            else:
                break
        next_root_left_child.right, next_root_right_child.left = (
            next_root.left,
            next_root.right,
        )
        next_root.left, next_root.right = self._header.right, self._header.left
        self._root = next_root

    _header: Node[_KeyT, _ValueT]
    _root: Node[_KeyT, _ValueT] | Nil

    __slots__ = '_header', 'root'

    def __init__(self, root: Node[_KeyT, _ValueT] | Nil) -> None:
        self._root = root
        self._header = Node(NotImplemented, NotImplemented)

    def __iter__(self, /) -> Iterator[Node[_KeyT, _ValueT]]:
        # we are collecting all values at once
        # because tree can be implicitly changed during iteration
        # (e.g. by simple lookup)
        # and cause infinite loops
        return cast(
            Iterator[Node[_KeyT, _ValueT]], iter(list(super().__iter__()))
        )

    def __reversed__(self, /) -> Iterator[Node[_KeyT, _ValueT]]:
        # we are collecting all values at once
        # because tree can be implicitly changed during iteration
        # (e.g. by simple lookup)
        # and cause infinite loops
        return cast(
            Iterator[Node[_KeyT, _ValueT]], iter(list(super().__reversed__()))
        )


def map_(*items: _Item[_KeyT, _ValueT]) -> _Map[_KeyT, _ValueT]:
    return _Map(Tree.from_components(*_split_items(items)))


@overload
def set_(*values: _ValueT, key: None = ...) -> _Set[_ValueT]: ...


@overload
def set_(
    *values: _ValueT, key: _Order[_ValueT, _KeyT]
) -> _KeyedSet[_KeyT, _ValueT]: ...


def set_(
    *values: _ValueT, key: _Order[_ValueT, _KeyT] | None = None
) -> _KeyedSet[_KeyT, _ValueT] | _Set[_ValueT]:
    return (
        _Set(Tree.from_components(values))
        if key is None
        else _KeyedSet(
            Tree.from_components([key(value) for value in values], values), key
        )
    )
