from __future__ import annotations

from collections.abc import Iterable
from typing import Generic, cast, overload

from reprit.base import generate_repr as _generate_repr
from typing_extensions import Self, override

from ._core import abcs, nil as _nil
from ._core.hints import (
    Item as _Item,
    KeyT as _KeyT,
    Order as _Order,
    ValueT as _ValueT,
)
from ._core.maps import Map as _Map
from ._core.sets import KeyedSet as _KeyedSet, Set as _Set
from ._core.utils import (
    are_keys_equal as _are_keys_equal,
    split_items as _split_items,
    to_unique_sorted_items as _to_unique_sorted_items,
    to_unique_sorted_values as _to_unique_sorted_values,
)

NIL = _nil.NIL
Nil = _nil.Nil


class Node(Generic[_KeyT, _ValueT]):
    @property
    def item(self, /) -> _Item[_KeyT, _ValueT]:
        return self.key, self.value

    @property
    def key(self, /) -> _KeyT:
        return self._key

    @property
    def left(self, /) -> Self | Nil:
        return self._left

    @left.setter
    def left(self, value: Self | Nil, /) -> None:
        self._left = value

    @property
    def right(self, /) -> Self | Nil:
        return self._right

    @right.setter
    def right(self, value: Self | Nil) -> None:
        self._right = value

    @property
    def value(self, /) -> _ValueT:
        return self._value

    @value.setter
    def value(self, value: _ValueT) -> None:
        self._value = value

    _left: Self | Nil
    _right: Self | Nil

    __slots__ = '_key', '_left', '_right', '_value'

    def __init__(
        self,
        key: _KeyT,
        value: _ValueT,
        /,
        *,
        left: Self | Nil = NIL,
        right: Self | Nil = NIL,
    ) -> None:
        self._key, self._value, self._left, self._right = (
            key,
            value,
            left,
            right,
        )

    __repr__ = _generate_repr(__init__)


class Tree(abcs.Tree[_KeyT, _ValueT]):
    @property
    def root(self, /) -> Node[_KeyT, _ValueT] | Nil:
        return self._root

    @overload
    @classmethod
    def from_components(
        cls, _keys: Iterable[_KeyT], _values: None = ...
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
                start_index: int, end_index: int, /
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

    @override
    def insert(self, key: _KeyT, value: _ValueT, /) -> Node[_KeyT, _ValueT]:
        parent = self._root
        if parent is NIL:
            node = self._root = Node(key, value)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = parent.left = Node(key, value)
                    return node
                parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = parent.right = Node(key, value)
                    return node
                parent = parent.right
            else:
                return parent

    @override
    def popmax(self, /) -> Node[_KeyT, _ValueT] | Nil:
        node = self._root
        if node is NIL:
            return node
        if node.right is NIL:
            self._root = node.left
            return node
        while node.right.right is not NIL:
            node = node.right
        assert node.right is not NIL
        result, node.right = node.right, node.right.left
        return result

    @override
    def popmin(self, /) -> Node[_KeyT, _ValueT] | Nil:
        node = self._root
        if node is NIL:
            return node
        if node.left is NIL:
            self._root = node.right
            return node
        while node.left.left is not NIL:
            node = node.left
        assert node.left is not NIL
        result, node.left = node.left, node.left.right
        return result

    @override
    def predecessor(
        self, node: abcs.Node[_KeyT, _ValueT], /
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
        return result

    @override
    def remove(self, node: abcs.Node[_KeyT, _ValueT], /) -> None:
        assert isinstance(node, Node), node
        assert self._root is not NIL
        parent, key = self._root, node.key
        if _are_keys_equal(key, parent.key):
            if parent.left is NIL:
                self._root = parent.right
            else:
                node = parent.left
                if node.right is NIL:
                    self._root, node.right = node, self._root.right
                else:
                    while node.right.right is not NIL:
                        node = node.right
                    assert node.right is not NIL
                    (
                        self._root,
                        node.right.left,
                        node.right.right,
                        node.right,
                    ) = (
                        node.right,
                        self._root.left,
                        self._root.right,
                        node.right.left,
                    )
            return
        while True:
            if key < parent.key:
                # search in left subtree
                assert parent.left is not NIL
                if _are_keys_equal(key, parent.left.key):
                    # remove `parent.left`
                    cursor = parent.left.left
                    if cursor is NIL:
                        parent.left = parent.left.right
                        return
                    if cursor.right is NIL:
                        parent.left, cursor.right = cursor, parent.left.right
                    else:
                        while cursor.right.right is not NIL:
                            cursor = cursor.right
                        assert cursor.right is not NIL
                        (
                            parent.left,
                            cursor.right.left,
                            cursor.right.right,
                            cursor.right,
                        ) = (
                            cursor.right,
                            parent.left.left,
                            parent.left.right,
                            cursor.right.left,
                        )
                    return
                parent = parent.left
            # search in right subtree
            else:
                assert parent.right is not NIL
                if _are_keys_equal(key, parent.right.key):
                    # remove `parent.right`
                    cursor = parent.right.left
                    if cursor is NIL:
                        parent.right = parent.right.right
                        return
                    if cursor.right is NIL:
                        parent.right, cursor.right = cursor, parent.right.right
                    else:
                        while cursor.right.right is not NIL:
                            cursor = cursor.right
                        assert cursor.right is not NIL
                        (
                            parent.right,
                            cursor.right.left,
                            cursor.right.right,
                            cursor.right,
                        ) = (
                            cursor.right,
                            parent.right.left,
                            parent.right.right,
                            cursor.right.left,
                        )
                    return
                parent = parent.right

    @override
    def successor(
        self, node: abcs.Node[_KeyT, _ValueT], /
    ) -> Node[_KeyT, _ValueT] | Nil:
        result: Node[_KeyT, _ValueT] | Nil
        assert isinstance(node, Node), node
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
        return result

    _root: Node[_KeyT, _ValueT] | Nil

    __slots__ = ('_root',)

    def __init__(self, root: Node[_KeyT, _ValueT] | Nil, /) -> None:
        self._root = root


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
