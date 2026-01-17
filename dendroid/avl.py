from __future__ import annotations

import copy as _copy
from collections.abc import Iterable as _Iterable
from reprlib import recursive_repr as _recursive_repr
from typing import Generic as _Generic, cast as _cast, overload as _overload

from reprit.base import generate_repr as _generate_repr
from typing_extensions import Self as _Self, override as _override

from ._core import abcs as _abcs
from ._core.hints import (
    Item as _Item,
    KeyT as _KeyT,
    Order as _Order,
    ValueT as _ValueT,
)
from ._core.maps import Map as _Map
from ._core.nil import NIL as _NIL, Nil as _Nil
from ._core.sets import KeyedSet as _KeyedSet, Set as _Set
from ._core.utils import (
    dereference_maybe as _dereference_maybe,
    maybe_weakref as _maybe_weakref,
    split_items as _split_items,
    to_unique_sorted_items as _to_unique_sorted_items,
    to_unique_sorted_values as _to_unique_sorted_values,
)

NIL = _NIL


class Node(_abcs.HasRepr, _Generic[_KeyT, _ValueT]):
    @property
    def balance_factor(self, /) -> int:
        return _to_height(self.left) - _to_height(self.right)

    @property
    def item(self, /) -> _Item[_KeyT, _ValueT]:
        return self.key, self.value

    @property
    def key(self, /) -> _KeyT:
        return self._key

    @property
    def left(self, /) -> _Self | _Nil:
        return self._left

    @left.setter
    def left(self, node: _Self | _Nil) -> None:
        self._left = node
        _set_parent(node, self)

    @property
    def parent(self, /) -> _Self | _Nil:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, value: _Self | _Nil, /) -> None:
        self._parent = _maybe_weakref(value)

    @property
    def right(self, /) -> _Self | _Nil:
        return self._right

    @right.setter
    def right(self, node: _Self | _Nil) -> None:
        self._right = node
        _set_parent(node, self)

    @property
    def value(self, /) -> _ValueT:
        return self._value

    @value.setter
    def value(self, value: _ValueT) -> None:
        self._value = value

    __slots__ = (
        '__weakref__',
        '_key',
        '_left',
        '_parent',
        '_right',
        '_value',
        'height',
    )

    def __init__(
        self,
        key: _KeyT,
        value: _ValueT,
        /,
        *,
        left: _Self | _Nil = NIL,
        right: _Self | _Nil = NIL,
        parent: _Self | _Nil = NIL,
    ) -> None:
        self._key, self._value = key, value
        self.left, self.right, self.parent = left, right, parent
        self.height = max(_to_height(self.left), _to_height(self.right)) + 1

    __repr__ = _recursive_repr()(_generate_repr(__init__))

    def __getstate__(
        self, /
    ) -> tuple[_KeyT, _ValueT, int, _Self | _Nil, _Self | _Nil, _Self | _Nil]:
        return (
            self._key,
            self._value,
            self.height,
            self.parent,
            self.left,
            self.right,
        )

    def __setstate__(
        self,
        state: tuple[
            _KeyT, _ValueT, int, _Self | _Nil, _Self | _Nil, _Self | _Nil
        ],
        /,
    ) -> None:
        (
            self._key,
            self._value,
            self.height,
            self.parent,
            self._left,
            self._right,
        ) = state


def _to_height(node: Node[_KeyT, _ValueT] | _Nil, /) -> int:
    return -1 if node is NIL else node.height


def _update_height(node: Node[_KeyT, _ValueT], /) -> None:
    node.height = max(_to_height(node.left), _to_height(node.right)) + 1


def _set_parent(
    node: Node[_KeyT, _ValueT] | _Nil, parent: Node[_KeyT, _ValueT] | _Nil, /
) -> None:
    if node is not NIL:
        node.parent = parent


class Tree(_abcs.Tree[_KeyT, _ValueT]):
    @property
    def root(self, /) -> Node[_KeyT, _ValueT] | _Nil:
        return self._root

    @_override
    def predecessor(
        self, node: _abcs.Node[_KeyT, _ValueT], /
    ) -> Node[_KeyT, _ValueT] | _Nil:
        assert isinstance(node, Node), node
        if node.left is NIL:
            result = node.parent
            while result is not NIL and node is result.left:
                node, result = result, result.parent
        else:
            result = node.left
            while result.right is not NIL:
                result = result.right
        return result

    @_override
    def successor(
        self, node: _abcs.Node[_KeyT, _ValueT], /
    ) -> Node[_KeyT, _ValueT] | _Nil:
        assert isinstance(node, Node), node
        if node.right is NIL:
            result = node.parent
            while result is not NIL and node is result.right:
                node, result = result, result.parent
        else:
            result = node.right
            while result.left is not NIL:
                result = result.left
        return result

    @_overload
    @classmethod
    def from_components(
        cls, keys: _Iterable[_KeyT], values: None = ..., /
    ) -> Tree[_KeyT, _KeyT]: ...

    @_overload
    @classmethod
    def from_components(
        cls, keys: _Iterable[_KeyT], values: _Iterable[_ValueT], /
    ) -> Tree[_KeyT, _ValueT]: ...

    @classmethod
    def from_components(
        cls: type[Tree[_KeyT, _KeyT]] | type[Tree[_KeyT, _ValueT]],
        keys: _Iterable[_KeyT],
        values: _Iterable[_ValueT] | None = None,
        /,
    ) -> Tree[_KeyT, _KeyT] | Tree[_KeyT, _ValueT]:
        keys = list(keys)
        if not keys:
            return cls(NIL)
        if values is None:
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

            return _cast(type[Tree[_KeyT, _KeyT]], cls)(
                to_simple_node(0, len(keys))
            )
        items = _to_unique_sorted_items(keys, list(values))

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

        return _cast(type[Tree[_KeyT, _ValueT]], cls)(
            to_complex_node(0, len(items))
        )

    @_override
    def clear(self, /) -> None:
        self._root = NIL

    @_override
    def insert(self, key: _KeyT, value: _ValueT, /) -> Node[_KeyT, _ValueT]:
        parent = self.root
        if parent is NIL:
            node = self._root = Node(key, value)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = Node(key, value)
                    parent.left = node
                    break
                parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = Node(key, value)
                    parent.right = node
                    break
                parent = parent.right
            else:
                return parent
        self._rebalance(node.parent)
        return node

    @_override
    def remove(self, node: _abcs.Node[_KeyT, _ValueT], /) -> None:
        assert isinstance(node, Node), node
        if node.left is NIL:
            imbalanced_node = node.parent
            self._transplant(node, node.right)
        elif node.right is NIL:
            imbalanced_node = node.parent
            self._transplant(node, node.left)
        else:
            successor = node.right
            while successor.left is not NIL:
                successor = successor.left
            if successor.parent is node:
                imbalanced_node = successor
            else:
                imbalanced_node = successor.parent
                self._transplant(successor, successor.right)
                successor.right = node.right
            self._transplant(node, successor)
            successor.left, successor.left.parent = node.left, successor
        self._rebalance(imbalanced_node)

    def _rebalance(self, node: Node[_KeyT, _ValueT] | _Nil) -> None:
        while node is not NIL:
            _update_height(node)
            if node.balance_factor > 1:
                assert node.left is not NIL
                if node.left.balance_factor < 0:
                    self._rotate_left(node.left)
                self._rotate_right(node)
            elif node.balance_factor < -1:
                assert node.right is not NIL
                if node.right.balance_factor > 0:
                    self._rotate_right(node.right)
                self._rotate_left(node)
            node = node.parent

    def _rotate_left(self, node: Node[_KeyT, _ValueT], /) -> None:
        replacement = node.right
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.right, replacement.left = replacement.left, node
        _update_height(node)
        _update_height(replacement)

    def _rotate_right(self, node: Node[_KeyT, _ValueT], /) -> None:
        replacement = node.left
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.left, replacement.right = replacement.right, node
        _update_height(node)
        _update_height(replacement)

    def _transplant(
        self,
        origin: Node[_KeyT, _ValueT],
        replacement: Node[_KeyT, _ValueT] | _Nil,
        /,
    ) -> None:
        parent = origin.parent
        if parent is _NIL:
            self._root = replacement
            _set_parent(replacement, _NIL)
        elif origin is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement

    _root: Node[_KeyT, _ValueT] | _Nil

    __slots__ = ('_root',)

    @_override
    def __copy__(self, /) -> _Self:
        return type(self)(_copy.deepcopy(self._root))

    def __init__(self, root: Node[_KeyT, _ValueT] | _Nil, /) -> None:
        self._root = root


def map_(*items: _Item[_KeyT, _ValueT]) -> _Map[_KeyT, _ValueT]:
    return _Map(Tree.from_components(*_split_items(items)))


@_overload
def set_(*values: _ValueT, key: None = ...) -> _Set[_ValueT]: ...


@_overload
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
