import sys as _sys
from functools import partial as _partial
from reprlib import recursive_repr as _recursive_repr
from typing import (Any as _Any,
                    Callable as _Callable,
                    Iterable as _Iterable,
                    Optional as _Optional,
                    Tuple as _Tuple,
                    Union as _Union)

from reprit.base import generate_repr as _generate_repr

from .core.abcs import (NIL,
                        AnyNode,
                        Node as _Node,
                        Tree as _Tree)
from .core.maps import map_constructor as _map_constructor
from .core.sets import set_constructor as _set_constructor
from .core.utils import (dereference_maybe as _dereference_maybe,
                         maybe_weakref as _maybe_weakref,
                         to_balanced_tree_height as _to_balanced_tree_height,
                         to_unique_sorted_items as _to_unique_sorted_items,
                         to_unique_sorted_values as _to_unique_sorted_values)
from .hints import (Key as _Key,
                    MapFactory as _MapFactory,
                    SetFactory as _SetFactory,
                    Value as _Value)


class Node(_Node):
    __slots__ = ('is_black', '_key', '_left', '_parent', '_right', '_value',
                 *(('__weakref__',) if _sys.version_info >= (3, 7) else ()))

    def __init__(self,
                 key: _Key,
                 value: _Union[_Key, _Value],
                 is_black: bool,
                 left: AnyNode = NIL,
                 right: AnyNode = NIL,
                 parent: AnyNode = None) -> None:
        self._key, self._value, self.is_black = key, value, is_black
        self.left, self.right, self.parent = left, right, parent

    __repr__ = _recursive_repr()(_generate_repr(__init__))

    State = _Tuple[_Any, ...]

    def __getstate__(self) -> State:
        return (self._key, self.value, self.is_black,
                self.parent, self.left, self.right)

    def __setstate__(self, state: State) -> None:
        (self._key, self._value, self.is_black,
         self.parent, self._left, self._right) = state

    @classmethod
    def from_simple(cls, key: _Key, *args: _Any) -> 'Node':
        return cls(key, key, *args)

    @property
    def key(self) -> _Key:
        return self._key

    @property
    def left(self) -> AnyNode:
        return self._left

    @left.setter
    def left(self, node: AnyNode) -> None:
        self._left = node
        _set_parent(node, self)

    @property
    def parent(self) -> AnyNode:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: AnyNode) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def right(self) -> AnyNode:
        return self._right

    @right.setter
    def right(self, node: AnyNode) -> None:
        self._right = node
        _set_parent(node, self)

    @property
    def value(self) -> _Value:
        return self._value

    @value.setter
    def value(self, value: _Value) -> None:
        self._value = value


def _set_parent(node: AnyNode, parent: _Optional[Node]) -> None:
    if node is not NIL:
        node.parent = parent


def _set_black(maybe_node: _Optional[Node]) -> None:
    if maybe_node is not None:
        maybe_node.is_black = True


def _is_left_child(node: Node) -> bool:
    parent = node.parent
    return parent is not None and parent.left is node


def _is_node_black(node: AnyNode) -> bool:
    return node is NIL or node.is_black


class Tree(_Tree[Node]):
    @staticmethod
    def predecessor(node: Node) -> AnyNode:
        if node.left is NIL:
            result = node.parent
            while result is not None and node is result.left:
                node, result = result, result.parent
        else:
            result = node.left
            while result.right is not NIL:
                result = result.right
        return result

    @staticmethod
    def successor(node: Node) -> AnyNode:
        if node.right is NIL:
            result = node.parent
            while result is not None and node is result.right:
                node, result = result, result.parent
        else:
            result = node.right
            while result.left is not NIL:
                result = result.left
        return result

    @classmethod
    def from_components(cls,
                        _keys: _Iterable[_Key],
                        _values: _Optional[
                            _Iterable[_Value]] = None) -> 'Tree':
        keys = list(_keys)
        if not keys:
            root = NIL
        elif _values is None:
            keys = _to_unique_sorted_values(keys)

            def to_node(start_index: int,
                        end_index: int,
                        depth: int,
                        height: int = _to_balanced_tree_height(len(keys)),
                        constructor: _Callable[..., Node] = Node.from_simple
                        ) -> Node:
                middle_index = (start_index + end_index) // 2
                return constructor(
                        keys[middle_index],
                        depth != height,
                        (to_node(start_index, middle_index, depth + 1)
                         if middle_index > start_index
                         else NIL),
                        (to_node(middle_index + 1, end_index, depth + 1)
                         if middle_index < end_index - 1
                         else NIL)
                )

            root = to_node(0, len(keys), 0)
            root.is_black = True
        else:
            items = _to_unique_sorted_items(keys, tuple(_values))

            def to_node(start_index: int,
                        end_index: int,
                        depth: int,
                        height: int = _to_balanced_tree_height(len(items)),
                        constructor: _Callable[..., Node] = Node) -> Node:
                middle_index = (start_index + end_index) // 2
                return constructor(
                        *items[middle_index],
                        depth != height,
                        (to_node(start_index, middle_index, depth + 1)
                         if middle_index > start_index
                         else NIL),
                        (to_node(middle_index + 1, end_index, depth + 1)
                         if middle_index < end_index - 1
                         else NIL)
                )

            root = to_node(0, len(items), 0)
            root.is_black = True
        return cls(root)

    def insert(self, key: _Key, value: _Value) -> Node:
        parent = self.root
        if parent is NIL:
            node = self.root = Node(key, value, True)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = Node(key, value, False)
                    parent.left = node
                    break
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = Node(key, value, False)
                    parent.right = node
                    break
                else:
                    parent = parent.right
            else:
                return parent
        self._restore(node)
        return node

    def remove(self, node: Node) -> None:
        successor, is_node_black = node, node.is_black
        if successor.left is NIL:
            (successor_child, successor_child_parent,
             is_successor_child_left) = (successor.right, successor.parent,
                                         _is_left_child(successor))
            self._transplant(successor, successor_child)
        elif successor.right is NIL:
            (successor_child, successor_child_parent,
             is_successor_child_left) = (successor.left, successor.parent,
                                         _is_left_child(successor))
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
            self._remove_node_fixup(successor_child, successor_child_parent,
                                    is_successor_child_left)

    def _restore(self, node: Node) -> None:
        while not _is_node_black(node.parent):
            parent = node.parent
            assert parent is not NIL
            grandparent = parent.parent
            if parent is grandparent.left:
                uncle = grandparent.right
                if _is_node_black(uncle):
                    if node is parent.right:
                        self._rotate_left(parent)
                        node, parent = parent, node
                    parent.is_black, grandparent.is_black = True, False
                    self._rotate_right(grandparent)
                else:
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
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
        assert self.root is not NIL
        self.root.is_black = True

    def _remove_node_fixup(self,
                           node: AnyNode,
                           parent: AnyNode,
                           is_left_child: bool) -> None:
        while node is not self.root and _is_node_black(node):
            assert parent is not NIL
            if is_left_child:
                sibling = parent.right
                assert sibling is not NIL
                if not _is_node_black(sibling):
                    sibling.is_black, parent.is_black = True, False
                    self._rotate_left(parent)
                    sibling = parent.right
                if (_is_node_black(sibling.left)
                        and _is_node_black(sibling.right)):
                    sibling.is_black = False
                    assert parent is not NIL
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.right):
                        sibling.left.is_black, sibling.is_black = True, False
                        self._rotate_right(sibling)
                        sibling = parent.right
                    sibling.is_black, parent.is_black = parent.is_black, True
                    _set_black(sibling.right)
                    self._rotate_left(parent)
                    node = self.root
            else:
                sibling = parent.left
                assert sibling is not NIL
                if not _is_node_black(sibling):
                    sibling.is_black, parent.is_black = True, False
                    self._rotate_right(parent)
                    sibling = parent.left
                if (_is_node_black(sibling.left)
                        and _is_node_black(sibling.right)):
                    sibling.is_black = False
                    assert parent is not NIL
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.left):
                        sibling.right.is_black, sibling.is_black = True, False
                        self._rotate_left(sibling)
                        sibling = parent.left
                    sibling.is_black, parent.is_black = parent.is_black, True
                    _set_black(sibling.left)
                    self._rotate_right(parent)
                    node = self.root
        _set_black(node)

    def _rotate_left(self, node: Node) -> None:
        replacement = node.right
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.right, replacement.left = replacement.left, node

    def _rotate_right(self, node: Node) -> None:
        replacement = node.left
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.left, replacement.right = replacement.right, node

    def _transplant(self, origin: Node, replacement: AnyNode) -> None:
        parent = origin.parent
        if parent is None:
            self.root = replacement
            _set_parent(replacement, None)
        elif origin is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement


map_: _MapFactory = _partial(_map_constructor, Tree.from_components)
set_: _SetFactory = _partial(_set_constructor, Tree.from_components)
