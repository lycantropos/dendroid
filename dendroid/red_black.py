from __future__ import annotations

import weakref as _weakref
from collections.abc import Iterable as _Iterable
from reprlib import recursive_repr as _recursive_repr
from typing import Any, Generic, cast, overload

from reprit.base import generate_repr as _generate_repr
from typing_extensions import Self as _Self, override as _override

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
    dereference_maybe as _dereference_maybe,
    maybe_weakref as _maybe_weakref,
    split_items as _split_items,
    to_balanced_tree_height as _to_balanced_tree_height,
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
    def left(self, /) -> _Self | Nil:
        return self._left

    @left.setter
    def left(self, node: _Self | Nil) -> None:
        self._left = node
        _set_parent(node, self)

    @property
    def parent(self, /) -> _Self | Nil:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: _Self | Nil) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def right(self, /) -> _Self | Nil:
        return self._right

    @right.setter
    def right(self, node: _Self | Nil) -> None:
        self._right = node
        _set_parent(node, self)

    @property
    def value(self, /) -> _ValueT:
        return self._value

    @value.setter
    def value(self, value: _ValueT) -> None:
        self._value = value

    _left: _Self | Nil
    _right: _Self | Nil
    _parent: _weakref.ref[_Self] | Nil

    __slots__ = (
        '__weakref__',
        '_key',
        '_left',
        '_parent',
        '_right',
        '_value',
        'is_black',
    )

    def __init__(
        self,
        key: _KeyT,
        value: _ValueT,
        /,
        *,
        is_black: bool,
        left: _Self | Nil = NIL,
        right: _Self | Nil = NIL,
        parent: _Self | Nil = NIL,
    ) -> None:
        self._key, self._value, self.is_black = key, value, is_black
        self.left, self.right, self.parent = left, right, parent

    __repr__ = _recursive_repr()(_generate_repr(__init__))

    def __getstate__(self, /) -> tuple[Any, ...]:
        return (
            self._key,
            self.value,
            self.is_black,
            self.parent,
            self.left,
            self.right,
        )

    def __setstate__(self, state: tuple[Any, ...]) -> None:
        (
            self._key,
            self._value,
            self.is_black,
            self.parent,
            self._left,
            self._right,
        ) = state


def _set_parent(
    node: Node[_KeyT, _ValueT] | Nil, parent: Node[_KeyT, _ValueT] | Nil
) -> None:
    if node is not NIL:
        node.parent = parent


def _set_black(node: Node[_KeyT, _ValueT] | Nil, /) -> None:
    if node is not NIL:
        node.is_black = True


def _is_left_child(node: Node[_KeyT, _ValueT], /) -> bool:
    parent = node.parent
    return parent is not NIL and parent.left is node


def _is_node_black(node: Node[_KeyT, _ValueT] | Nil, /) -> bool:
    return node is NIL or node.is_black


class Tree(_abcs.Tree[_KeyT, _ValueT]):
    root: Node[_KeyT, _ValueT] | Nil

    @_override
    def predecessor(
        self, node: _abcs.Node[_KeyT, _ValueT], /
    ) -> Node[_KeyT, _ValueT] | Nil:
        assert isinstance(node, Node)
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
    ) -> Node[_KeyT, _ValueT] | Nil:
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

    @overload
    @classmethod
    def from_components(
        cls, _keys: _Iterable[_KeyT], _values: None = ...
    ) -> Tree[_KeyT, _KeyT]: ...

    @overload
    @classmethod
    def from_components(
        cls, _keys: _Iterable[_KeyT], _values: _Iterable[_ValueT]
    ) -> _Self: ...

    @classmethod
    def from_components(
        cls: type[Tree[_KeyT, _KeyT]] | type[Tree[_KeyT, _ValueT]],
        _keys: _Iterable[_KeyT],
        _values: _Iterable[_ValueT] | None = None,
    ) -> Tree[_KeyT, _KeyT] | Tree[_KeyT, _ValueT]:
        keys = list(_keys)
        if not keys:
            return cls(NIL)
        if _values is None:
            keys = _to_unique_sorted_values(keys)

            def to_simple_node(
                start_index: int,
                end_index: int,
                depth: int,
                height: int = _to_balanced_tree_height(len(keys)),
            ) -> Node[_KeyT, _KeyT]:
                middle_index = (start_index + end_index) // 2
                key = keys[middle_index]
                return Node(
                    key,
                    key,
                    is_black=depth != height,
                    left=(
                        to_simple_node(start_index, middle_index, depth + 1)
                        if middle_index > start_index
                        else NIL
                    ),
                    right=(
                        to_simple_node(middle_index + 1, end_index, depth + 1)
                        if middle_index < end_index - 1
                        else NIL
                    ),
                )

            simple_root = to_simple_node(0, len(keys), 0)
            simple_root.is_black = True
            return cast(type[Tree[_KeyT, _KeyT]], cls)(simple_root)
        items = _to_unique_sorted_items(keys, tuple(_values))

        def to_complex_node(
            start_index: int,
            end_index: int,
            depth: int,
            height: int = _to_balanced_tree_height(len(items)),
            /,
        ) -> Node[_KeyT, _ValueT]:
            middle_index = (start_index + end_index) // 2
            key, value = items[middle_index]
            return Node(
                key,
                value,
                is_black=depth != height,
                left=(
                    to_complex_node(start_index, middle_index, depth + 1)
                    if middle_index > start_index
                    else NIL
                ),
                right=(
                    to_complex_node(middle_index + 1, end_index, depth + 1)
                    if middle_index < end_index - 1
                    else NIL
                ),
            )

        complex_root = to_complex_node(0, len(items), 0)
        complex_root.is_black = True
        return cast(type[Tree[_KeyT, _ValueT]], cls)(complex_root)

    def insert(self, key: _KeyT, value: _ValueT, /) -> Node[_KeyT, _ValueT]:
        parent = self.root
        if parent is NIL:
            node = self.root = Node(key, value, is_black=True)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = Node(key, value, is_black=False)
                    parent.left = node
                    break
                parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = Node(key, value, is_black=False)
                    parent.right = node
                    break
                parent = parent.right
            else:
                return parent
        self._restore(node)
        return node

    def remove(self, node: _abcs.Node[_KeyT, _ValueT]) -> None:
        assert isinstance(node, Node)
        successor, is_node_black = node, node.is_black
        if successor.left is NIL:
            (
                successor_child,
                successor_child_parent,
                is_successor_child_left,
            ) = (successor.right, successor.parent, _is_left_child(successor))
            self._transplant(successor, successor_child)
        elif successor.right is NIL:
            (
                successor_child,
                successor_child_parent,
                is_successor_child_left,
            ) = (successor.left, successor.parent, _is_left_child(successor))
            self._transplant(successor, successor_child)
        else:
            assert node.right is not NIL
            successor = node.right
            while successor.left is not NIL:
                successor = successor.left
            is_node_black = successor.is_black
            successor_child, is_successor_child_left = successor.right, False
            if successor.parent is node:
                successor_child_parent = successor
            else:
                is_successor_child_left = _is_left_child(successor)
                successor_child_parent = successor.parent
                self._transplant(successor, successor.right)
                successor.right = node.right
            self._transplant(node, successor)
            assert node.left is not NIL
            node.left.parent = successor
            successor.left, successor.is_black = node.left, node.is_black
        if is_node_black:
            self._remove_node_fixup(
                successor_child,
                successor_child_parent,
                is_successor_child_left,
            )

    def _restore(self, node: Node[_KeyT, _ValueT]) -> None:
        while not _is_node_black(node.parent):
            parent = node.parent
            assert parent is not NIL
            grandparent = parent.parent
            assert grandparent is not NIL
            if parent is grandparent.left:
                uncle = grandparent.right
                if _is_node_black(uncle):
                    if node is parent.right:
                        self._rotate_left(parent)
                        node, parent = parent, node
                    parent.is_black, grandparent.is_black = True, False
                    self._rotate_right(grandparent)
                else:
                    assert uncle is not NIL
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
            else:
                uncle = grandparent.left
                if _is_node_black(uncle):
                    if node is parent.left:
                        self._rotate_right(parent)
                        node, parent = parent, node
                    parent.is_black, grandparent.is_black = True, False
                    self._rotate_left(grandparent)
                else:
                    assert uncle is not NIL
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
        assert self.root is not NIL
        self.root.is_black = True

    def _remove_node_fixup(
        self,
        node: Node[_KeyT, _ValueT] | Nil,
        parent: Node[_KeyT, _ValueT] | Nil,
        is_left_child: bool,  # noqa: FBT001
        /,
    ) -> None:
        while node is not self.root and _is_node_black(node):
            assert parent is not NIL
            if is_left_child:
                sibling = parent.right
                assert sibling is not NIL
                if not _is_node_black(sibling):
                    sibling.is_black, parent.is_black = True, False
                    self._rotate_left(parent)
                    sibling = parent.right
                assert sibling is not NIL
                if _is_node_black(sibling.left) and _is_node_black(
                    sibling.right
                ):
                    sibling.is_black = False
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.right):
                        assert sibling.left is not NIL
                        sibling.left.is_black, sibling.is_black = True, False
                        self._rotate_right(sibling)
                        sibling = parent.right
                    assert sibling is not NIL
                    sibling.is_black, parent.is_black = parent.is_black, True
                    _set_black(sibling.right)
                    self._rotate_left(parent)
                    node = self.root
            else:
                sibling = parent.left
                if not _is_node_black(sibling):
                    assert sibling is not NIL
                    sibling.is_black, parent.is_black = True, False
                    self._rotate_right(parent)
                    sibling = parent.left
                assert sibling is not NIL
                if _is_node_black(sibling.left) and _is_node_black(
                    sibling.right
                ):
                    sibling.is_black = False
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.left):
                        assert sibling.right is not NIL
                        sibling.right.is_black, sibling.is_black = True, False
                        self._rotate_left(sibling)
                        sibling = parent.left
                    assert sibling is not NIL
                    sibling.is_black, parent.is_black = parent.is_black, True
                    _set_black(sibling.left)
                    self._rotate_right(parent)
                    node = self.root
        _set_black(node)

    def _rotate_left(self, node: Node[_KeyT, _ValueT]) -> None:
        replacement = node.right
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.right, replacement.left = replacement.left, node

    def _rotate_right(self, node: Node[_KeyT, _ValueT]) -> None:
        replacement = node.left
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.left, replacement.right = replacement.right, node

    def _transplant(
        self,
        origin: Node[_KeyT, _ValueT],
        replacement: Node[_KeyT, _ValueT] | Nil,
    ) -> None:
        parent = origin.parent
        if parent is NIL:
            self.root = replacement
            _set_parent(replacement, NIL)
        elif origin is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement

    __slots__ = ('root',)

    def __init__(self, root: Node[_KeyT, _ValueT] | Nil) -> None:
        self.root = root


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
