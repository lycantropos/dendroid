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
                         to_unique_sorted_items as _to_unique_sorted_items,
                         to_unique_sorted_values as _to_unique_sorted_values)
from .hints import (Key as _Key,
                    MapFactory as _MapFactory,
                    SetFactory as _SetFactory,
                    Value as _Value)


class Node(_Node):
    __slots__ = ('height', '_key', '_left', '_parent', '_right', '_value',
                 *(('__weakref__',) if _sys.version_info >= (3, 7) else ()))

    def __init__(self,
                 key: _Key,
                 value: _Union[_Key, _Value],
                 left: AnyNode = NIL,
                 right: AnyNode = NIL,
                 parent: AnyNode = None) -> None:
        self._key, self._value = key, value
        self.left, self.right, self.parent = left, right, parent
        self.height = max(_to_height(self.left), _to_height(self.right)) + 1

    __repr__ = _recursive_repr()(_generate_repr(__init__))

    State = _Tuple[_Key, _Value, int, AnyNode, AnyNode, AnyNode]

    def __getstate__(self) -> State:
        return (self._key, self._value, self.height,
                self.parent, self.left, self.right)

    def __setstate__(self, state: State) -> None:
        (self._key, self._value, self.height,
         self.parent, self._left, self._right) = state

    @classmethod
    def from_simple(cls, key: _Key, *args: _Any) -> 'Node':
        return cls(key, key, *args)

    @property
    def balance_factor(self) -> int:
        return _to_height(self.left) - _to_height(self.right)

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


def _to_height(node: AnyNode) -> int:
    return -1 if node is NIL else node.height


def _update_height(node: Node) -> None:
    node.height = max(_to_height(node.left), _to_height(node.right)) + 1


def _set_parent(node: AnyNode, parent: _Optional[Node]) -> None:
    if node is not NIL:
        node.parent = parent


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
                        constructor: _Callable[..., Node] = Node.from_simple
                        ) -> Node:
                middle_index = (start_index + end_index) // 2
                return constructor(keys[middle_index],
                                   (to_node(start_index, middle_index)
                                    if middle_index > start_index
                                    else NIL),
                                   (to_node(middle_index + 1, end_index)
                                    if middle_index < end_index - 1
                                    else NIL))

            root = to_node(0, len(keys))
        else:
            items = _to_unique_sorted_items(keys, list(_values))

            def to_node(start_index: int,
                        end_index: int,
                        constructor: _Callable[..., Node] = Node) -> Node:
                middle_index = (start_index + end_index) // 2
                return constructor(*items[middle_index],
                                   (to_node(start_index, middle_index)
                                    if middle_index > start_index
                                    else NIL),
                                   (to_node(middle_index + 1, end_index)
                                    if middle_index < end_index - 1
                                    else NIL))

            root = to_node(0, len(items))
        return cls(root)

    def insert(self, key: _Key, value: _Value) -> Node:
        parent = self.root
        if parent is NIL:
            node = self.root = Node(key, value)
            return node
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = Node(key, value)
                    parent.left = node
                    break
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = Node(key, value)
                    parent.right = node
                    break
                else:
                    parent = parent.right
            else:
                return parent
        self._rebalance(node.parent)
        return node

    def remove(self, node: Node) -> None:
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

    def _rebalance(self, node: AnyNode) -> None:
        while node is not None:
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

    def _rotate_left(self, node: Node) -> None:
        replacement = node.right
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.right, replacement.left = replacement.left, node
        _update_height(node)
        _update_height(replacement)

    def _rotate_right(self, node: Node) -> None:
        replacement = node.left
        assert replacement is not NIL
        self._transplant(node, replacement)
        node.left, replacement.right = replacement.right, node
        _update_height(node)
        _update_height(replacement)

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
