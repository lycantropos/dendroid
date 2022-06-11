from functools import partial
from typing import (Callable,
                    Iterable,
                    Iterator,
                    Optional, Union)

from .binary import Node
from .core.abcs import (NIL,
                        Nil,
                        Tree as _Tree)
from .core.maps import map_constructor as _map_constructor
from .core.sets import set_constructor as _set_constructor
from .core.utils import (to_unique_sorted_items as _to_unique_sorted_items,
                         to_unique_sorted_values as _to_unique_sorted_values)
from .hints import (Key,
                    MapFactory,
                    SetFactory,
                    Value)

Node = Node


class Tree(_Tree[Node]):
    __slots__ = '_header',

    def __init__(self, root: Union[Nil, Node]) -> None:
        super().__init__(root)
        self._header = Node(None, None)

    def __iter__(self) -> Iterator[Node]:
        # we are collecting all values at once
        # because tree can be implicitly changed during iteration
        # (e.g. by simple lookup)
        # and cause infinite loops
        return iter(list(super().__iter__()))

    def __reversed__(self) -> Iterator[Node]:
        # we are collecting all values at once
        # because tree can be implicitly changed during iteration
        # (e.g. by simple lookup)
        # and cause infinite loops
        return iter(list(super().__reversed__()))

    @classmethod
    def from_components(cls,
                        _keys: Iterable[Key],
                        _values: Optional[Iterable[Value]] = None) -> 'Tree':
        keys = list(_keys)
        if not keys:
            root = NIL
        elif _values is None:
            keys = _to_unique_sorted_values(keys)

            def to_node(start_index: int,
                        end_index: int,
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
            items = _to_unique_sorted_items(keys, tuple(_values))

            def to_node(start_index: int,
                        end_index: int,
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

    def find(self, key: Key) -> Union[Nil, Node]:
        if self.root is NIL:
            return NIL
        self._splay(key)
        root = self.root
        return NIL if key < root.key or root.key < key else root

    def insert(self, key: Key, value: Value) -> Node:
        if self.root is NIL:
            node = self.root = Node(key, value)
            return node
        self._splay(key)
        if key < self.root.key:
            self.root.left, self.root = NIL, Node(key, value, self.root.left,
                                                  self.root)
        elif self.root.key < key:
            self.root.right, self.root = NIL, Node(key, value, self.root,
                                                   self.root.right)
        return self.root

    def max(self) -> Union[Nil, Node]:
        node = self.root
        if node is not NIL:
            while node.right is not NIL:
                node = node.right
                assert node is not NIL
            self._splay(node.key)
        return node

    def min(self) -> Union[Nil, Node]:
        node = self.root
        if node is not NIL:
            while node.left is not NIL:
                node = node.left
                assert node is not NIL
            self._splay(node.key)
        return node

    def popmax(self) -> Union[Nil, Node]:
        if self.root is NIL:
            return self.root
        result = self.max()
        self._remove_root()
        return result

    def popmin(self) -> Union[Nil, Node]:
        if self.root is NIL:
            return self.root
        result = self.min()
        self._remove_root()
        return result

    def predecessor(self, node: Node) -> Union[Nil, Node]:
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
            assert result is not NIL
            while result.right is not NIL:
                result = result.right
                assert result is not NIL
        if result is not NIL:
            self._splay(result.key)
        return result

    def remove(self, node: Node) -> None:
        self._splay(node.key)
        self._remove_root()

    def successor(self, node: Node) -> Union[Nil, Node]:
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
        if result is not NIL:
            self._splay(result.key)
        return result

    def _splay(self, key: Key) -> None:
        next_root = self.root
        next_root_left_child = next_root_right_child = self._header
        while True:
            assert next_root is not NIL
            if key < next_root.key:
                if next_root.left is NIL:
                    break
                elif key < next_root.left.key:
                    next_root = self._rotate_right(next_root)
                    if next_root.left is NIL:
                        break
                next_root_right_child.left = next_root
                next_root_right_child, next_root = next_root, next_root.left
            elif next_root.key < key:
                if next_root.right is NIL:
                    break
                elif next_root.right.key < key:
                    next_root = self._rotate_left(next_root)
                    if next_root.right is NIL:
                        break
                next_root_left_child.right = next_root
                next_root_left_child, next_root = next_root, next_root.right
            else:
                break
        assert next_root is not NIL
        next_root_left_child.right, next_root_right_child.left = (
            next_root.left, next_root.right
        )
        next_root.left, next_root.right = self._header.right, self._header.left
        self.root = next_root

    def _remove_root(self) -> None:
        root = self.root
        assert root is not NIL
        if root.left is NIL:
            self.root = root.right
        else:
            right_root_child = root.right
            self.root = root.left
            self._splay(root.key)
            assert self.root is not NIL
            self.root.right = right_root_child

    @staticmethod
    def _rotate_left(node: Node) -> Node:
        replacement = node.right
        assert replacement is not NIL
        node.right, replacement.left = replacement.left, node
        return replacement

    @staticmethod
    def _rotate_right(node: Node) -> Node:
        replacement = node.left
        assert replacement is not NIL
        node.left, replacement.right = replacement.right, node
        return replacement


map_ = partial(_map_constructor, Tree.from_components)  # type: MapFactory
set_ = partial(_set_constructor, Tree.from_components)  # type: SetFactory
