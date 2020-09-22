from functools import partial
from typing import (Any,
                    Callable,
                    Iterable,
                    Optional,
                    Union)

from reprit.base import generate_repr

from .abcs import (NIL,
                   AnyNode,
                   Node as NodeBase,
                   Tree as TreeBase)
from .hints import (Key,
                    Value)
from .mappings import to_map_constructor
from .sets import set_constructor
from .utils import (_to_unique_sorted_items,
                    _to_unique_sorted_values,
                    are_keys_equal)


class Node(NodeBase):
    __slots__ = '_key', '_value', 'left', 'right'

    def __init__(self,
                 key: Key,
                 value: Value,
                 left: Union[NIL, 'Node'] = NIL,
                 right: Union[NIL, 'Node'] = NIL) -> None:
        self._key, self._value, self.left, self.right = key, value, left, right

    __repr__ = generate_repr(__init__)

    @classmethod
    def from_simple(cls, key: Key, *args: Any) -> 'Node':
        return cls(key, key, *args)

    @property
    def key(self) -> Key:
        return self._key

    @property
    def value(self) -> Value:
        return self._value

    @value.setter
    def value(self, value: Value) -> None:
        self._value = value


class Tree(TreeBase[Key, Value]):
    @classmethod
    def from_components(cls,
                        keys: Iterable[Key],
                        values: Optional[Iterable[Value]] = None
                        ) -> 'Tree[Key, Value]':
        keys = list(keys)
        if not keys:
            root = NIL
        elif values is None:
            keys = _to_unique_sorted_values(keys)

            def to_node(start_index: int, end_index: int,
                        constructor: Callable[..., Node] = Node.from_simple
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
            items = _to_unique_sorted_items(keys, list(values))

            def to_node(start_index: int, end_index: int,
                        constructor: Callable[..., Node] = Node) -> Node:
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

    def insert(self, key: Key, value: Value) -> AnyNode:
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

    def remove(self, node: Node) -> None:
        parent = self.root
        if parent is NIL:
            return
        key = node.key
        if are_keys_equal(key, parent.key):
            if parent.left is NIL:
                self.root = parent.right
            else:
                node = parent.left
                if node.right is NIL:
                    self.root, node.right = node, self.root.right
                else:
                    while node.right.right is not NIL:
                        node = node.right
                    (self.root, node.right.left, node.right.right,
                     node.right) = (
                        node.right, self.root.left, self.root.right,
                        node.right.left)
            return
        while True:
            if key < parent.key:
                # search in left subtree
                if parent.left is NIL:
                    return
                elif key < parent.left.key:
                    parent = parent.left
                else:
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
                        (parent.left, node.right.left, node.right.right,
                         node.right) = (
                            node.right, parent.left.left, parent.left.right,
                            node.right.left)
            else:
                # search in right subtree
                if parent.right is NIL:
                    return
                elif parent.right.key < key:
                    parent = parent.right
                else:
                    # remove `parent.right`
                    node = parent.right.left
                    if node is NIL:
                        parent.right = parent.right.right
                        return
                    elif node.right is NIL:
                        parent.right, node.right = node, parent.right.right
                    else:
                        while node.right.right is not NIL:
                            node = node.right
                        (parent.right, node.right.left, node.right.right,
                         node.right) = (
                            node.right, parent.right.left, parent.right.right,
                            node.right.left)

    def popmax(self) -> Node:
        node = self.root
        if node is NIL:
            raise KeyError
        elif node.right is NIL:
            self.root = node.left
            return node
        else:
            while node.right.right is not NIL:
                node = node.right
            result, node.right = node.right, node.right.left
            return result

    def popmin(self) -> Node:
        node = self.root
        if node is NIL:
            raise KeyError
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
            candidate, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                if cursor.key < key:
                    candidate, cursor = cursor, cursor.right
                else:
                    cursor = cursor.left
            return candidate
        else:
            result = node.left
            while result.right is not NIL:
                result = result.right
            return result

    def successor(self, node: Node) -> AnyNode:
        if node.right is NIL:
            candidate, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                if key < cursor.key:
                    candidate, cursor = cursor, cursor.left
                else:
                    cursor = cursor.right
            return candidate
        else:
            result = node.right
            while result.left is not NIL:
                result = result.left
            return result


map_ = to_map_constructor(Tree.from_components)
set_ = partial(set_constructor, Tree.from_components)
