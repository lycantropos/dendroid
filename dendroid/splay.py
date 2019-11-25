from typing import (Iterable,
                    Optional,
                    Union)

from reprit.base import generate_repr

from .binary import (NIL,
                     Node,
                     TreeBase,
                     _to_unique_sorted_items,
                     _to_unique_sorted_values)
from .hints import (Domain,
                    Sortable,
                    SortingKey)


class SimpleNode(Node):
    __slots__ = ('_value', 'left', 'right')

    def __init__(self, value: Domain,
                 *,
                 left: Union['SimpleNode', NIL] = NIL,
                 right: Union['SimpleNode', NIL] = NIL) -> None:
        self._value = value
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._value


class ComplexNode(Node):
    __slots__ = ('_key', '_value', 'left', 'right')

    def __init__(self, key: Sortable, value: Domain,
                 *,
                 left: Union['ComplexNode', NIL] = NIL,
                 right: Union['ComplexNode', NIL] = NIL) -> None:
        self._value = value
        self._key = key
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._key


class Tree(TreeBase[Domain]):
    __slots__ = ('_root', '_key', '_header')

    def __init__(self, root: Union[Node, NIL],
                 *,
                 key: Optional[SortingKey]) -> None:
        self._root = root
        self._key = key
        self._header = SimpleNode(None)

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def root(self) -> Union[Node, NIL]:
        return self._root

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    def __contains__(self, value: Domain) -> bool:
        if self.root is NIL:
            return False
        key = self._to_key(value)
        self._splay(key)
        return self.root.key == key

    def max(self) -> Domain:
        node = self.root
        if node is NIL:
            raise ValueError('Tree is empty.')
        while node.right is not NIL:
            node = node.right
        self._splay(node.key)
        return node.value

    def min(self) -> Domain:
        node = self.root
        if node is NIL:
            raise ValueError('Tree is empty.')
        while node.left is not NIL:
            node = node.left
        self._splay(node.key)
        return node.value

    def add(self, value: Domain) -> None:
        if self._root is NIL:
            self._root = self._make_node(value)
            return
        key = self._to_key(value)
        self._splay(key)
        if key == self._root.key:
            return
        node = self._make_node(value)
        if key < self._root.key:
            node.left, node.right, self._root.left = (
                self._root.left, self._root, NIL)
        else:
            node.left, node.right, self._root.right = (
                self._root, self._root.right, NIL)
        self._root = node

    def discard(self, value: Domain) -> None:
        if self._root is NIL:
            return
        key = self._to_key(value)
        self._splay(key)
        if key != self._root.key:
            return
        self._remove_root(key)

    def popmax(self) -> Domain:
        if self._root is NIL:
            raise KeyError
        result = self.max()
        self.discard(result)
        return result

    def popmin(self) -> Domain:
        if self._root is NIL:
            raise KeyError
        result = self.min()
        self.discard(result)
        return result

    def clear(self) -> None:
        self._root = NIL

    @classmethod
    def from_iterable(cls, values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'Tree[Domain]':
        values = list(values)
        if not values:
            root = NIL
        elif key is None:
            values = _to_unique_sorted_values(values)

            def to_node(start_index: int, end_index: int) -> SimpleNode:
                middle_index = (start_index + end_index) // 2
                return SimpleNode(values[middle_index],
                                  left=(to_node(start_index, middle_index)
                                        if middle_index > start_index
                                        else NIL),
                                  right=(
                                      to_node(middle_index + 1, end_index)
                                      if middle_index < end_index - 1
                                      else NIL))

            root = to_node(0, len(values))
        else:
            items = _to_unique_sorted_items(values, key)

            def to_node(start_index: int, end_index: int) -> ComplexNode:
                middle_index = (start_index + end_index) // 2
                return ComplexNode(*items[middle_index],
                                   left=(to_node(start_index, middle_index)
                                         if middle_index > start_index
                                         else NIL),
                                   right=(
                                       to_node(middle_index + 1, end_index)
                                       if middle_index < end_index - 1
                                       else NIL))

            root = to_node(0, len(items))
        return cls(root,
                   key=key)

    def _splay(self, key: Sortable) -> None:
        next_root = self._root
        self._header.left = self._header.right = NIL
        next_root_left_child = next_root_right_child = self._header
        while True:
            if key < next_root.key:
                if next_root.left is NIL:
                    break
                elif key < next_root.left.key:
                    next_root = self._rotate_right(next_root)
                    if next_root.left is NIL:
                        break
                next_root_right_child.left = next_root
                next_root_right_child, next_root = next_root, next_root.left
            elif key > next_root.key:
                if next_root.right is NIL:
                    break
                elif key > next_root.right.key:
                    next_root = self._rotate_left(next_root)
                    if next_root.right is NIL:
                        break
                next_root_left_child.right = next_root
                next_root_left_child, next_root = next_root, next_root.right
            else:
                break
        next_root_left_child.right = next_root.left
        next_root_right_child.left = next_root.right
        next_root.left, next_root.right = self._header.right, self._header.left
        self._root = next_root

    def _make_node(self, value: Domain) -> Node:
        if self._key is None:
            return SimpleNode(value)
        else:
            return ComplexNode(self._key(value), value)

    def _remove_root(self, key: Sortable) -> None:
        root = self._root
        if root.left is NIL:
            self._root = root.right
        else:
            right_root_child = root.right
            self._root = root.left
            self._splay(key)
            self._root.right = right_root_child

    @staticmethod
    def _rotate_left(node: Node) -> Union[NIL, Node]:
        replacement = node.right
        node.right, replacement.left = replacement.left, node
        return replacement

    @staticmethod
    def _rotate_right(node: Node) -> Union[NIL, Node]:
        replacement = node.left
        node.left, replacement.right = replacement.right, node
        return replacement

    def _to_key(self, value: Domain) -> Sortable:
        return value if self._key is None else self._key(value)


def tree(*values: Domain, key: Optional[SortingKey] = None) -> Tree[Domain]:
    return Tree.from_iterable(values,
                              key=key)
