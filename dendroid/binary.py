from functools import partial as _partial
from typing import (Any as _Any,
                    Callable as _Callable,
                    Iterable as _Iterable,
                    Optional as _Optional,
                    Union as _Union)

from reprit.base import generate_repr as _generate_repr

from .core.abcs import (NIL,
                        AnyNode,
                        Node as _Node,
                        Tree as _Tree)
from .core.maps import map_constructor as _map_constructor
from .core.sets import set_constructor as _set_constructor
from .core.utils import (are_keys_equal as _are_keys_equal,
                         to_unique_sorted_items as _to_unique_sorted_items,
                         to_unique_sorted_values as _to_unique_sorted_values)
from .hints import (Key as _Key,
                    MapFactory as _MapFactory,
                    SetFactory as _SetFactory,
                    Value as _Value)


class Node(_Node):
    __slots__ = '_left', '_right', '_key', '_value'

    def __init__(self,
                 key: _Key,
                 value: _Union[_Key, _Value],
                 left: AnyNode = NIL,
                 right: AnyNode = NIL) -> None:
        self._key, self._value, self._left, self._right = (
            key, value, left, right
        )

    __repr__ = _generate_repr(__init__)

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
    def left(self, value: AnyNode) -> None:
        self._left = value

    @property
    def right(self) -> AnyNode:
        return self._right

    @right.setter
    def right(self, value: AnyNode) -> None:
        self._right = value

    @property
    def value(self) -> _Value:
        return self._value

    @value.setter
    def value(self, value: _Value) -> None:
        self._value = value


class Tree(_Tree[Node]):
    @classmethod
    def from_components(cls,
                        _keys: _Iterable[_Key],
                        _values: _Optional[_Iterable[_Value]] = None
                        ) -> 'Tree':
        keys = list(_keys)
        if not keys:
            root = NIL
        elif _values is None:
            keys = _to_unique_sorted_values(keys)

            def to_node(start_index: int, end_index: int,
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
            items = _to_unique_sorted_items(keys, tuple(_values))

            def to_node(start_index: int, end_index: int,
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
                    node = parent.left = Node(key, value)
                    return node
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = parent.right = Node(key, value)
                    return node
                else:
                    parent = parent.right
            else:
                return parent

    def popmax(self) -> AnyNode:
        node = self.root
        if node is NIL:
            return node
        elif node.right is NIL:
            self.root = node.left
            return node
        else:
            while node.right.right is not NIL:
                node = node.right
            result, node.right = node.right, node.right.left
            return result

    def popmin(self) -> AnyNode:
        node = self.root
        if node is NIL:
            return node
        elif node.left is NIL:
            self.root = node.right
            return node
        else:
            while node.left.left is not NIL:
                node = node.left
            result, node.left = node.left, node.left.right
            return result

    def predecessor(self, node: Node) -> AnyNode:
        if node.left is NIL:
            result, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                assert cursor is not NIL
                if cursor.key < key:
                    result, cursor = cursor, cursor.right
                else:
                    cursor = cursor.left
        else:
            result = node.left
            while result.right is not NIL:
                result = result.right
        return result

    def remove(self, node: Node) -> None:
        assert self.root is not NIL
        parent, key = self.root, node.key
        if _are_keys_equal(key, parent.key):
            if parent.left is NIL:
                self.root = parent.right
            else:
                node = parent.left
                if node.right is NIL:
                    self.root, node.right = node, self.root.right
                else:
                    while node.right.right is not NIL:
                        node = node.right
                    assert node.right is not NIL
                    (self.root, node.right.left, node.right.right,
                     node.right) = (node.right, self.root.left,
                                    self.root.right, node.right.left)
            return
        while True:
            assert parent is not NIL
            if key < parent.key:
                # search in left subtree
                assert parent.left is not NIL
                if _are_keys_equal(key, parent.left.key):
                    # remove `parent.left`
                    node = parent.left.left
                    if node is NIL:
                        parent.left = parent.left.right
                        return
                    elif node.right is NIL:
                        parent.left, node.right = node, parent.left.right
                    else:
                        while node.right.right is not NIL:
                            node = node.right
                        assert node.right is not NIL
                        (parent.left, node.right.left, node.right.right,
                         node.right) = (node.right, parent.left.left,
                                        parent.left.right, node.right.left)
                    return
                else:
                    parent = parent.left
            # search in right subtree
            else:
                assert parent.right is not NIL
                if _are_keys_equal(key, parent.right.key):
                    # remove `parent.right`
                    assert parent.right is not NIL
                    node = parent.right.left
                    if node is NIL:
                        parent.right = parent.right.right
                        return
                    elif node.right is NIL:
                        parent.right, node.right = node, parent.right.right
                    else:
                        while node.right.right is not NIL:
                            node = node.right
                        assert node.right is not NIL
                        (
                            parent.right, node.right.left, node.right.right,
                            node.right
                        ) = (
                            node.right, parent.right.left, parent.right.right,
                            node.right.left
                        )
                    return
                else:
                    parent = parent.right

    def successor(self, node: Node) -> AnyNode:
        if node.right is NIL:
            result, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                assert cursor is not NIL
                if key < cursor.key:
                    result, cursor = cursor, cursor.left
                else:
                    cursor = cursor.right
        else:
            result = node.right
            assert result is not NIL
            while result.left is not NIL:
                result = result.left
                assert result is not NIL
        return result


map_: _MapFactory = _partial(_map_constructor, Tree.from_components)
set_: _SetFactory = _partial(_set_constructor, Tree.from_components)
