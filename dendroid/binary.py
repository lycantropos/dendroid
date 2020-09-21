from typing import (Iterable,
                    Optional,
                    Union)

from reprit.base import generate_repr

from .base import (NIL,
                   Node,
                   TreeBase)
from .hints import (Domain,
                    Sortable,
                    SortingKey)
from .utils import (_to_unique_sorted_items,
                    _to_unique_sorted_values)


class SimpleNode(Node):
    __slots__ = ('_value', 'left', 'right')

    def __init__(self, value: Domain,
                 *,
                 left: Union[NIL, 'SimpleNode'] = NIL,
                 right: Union[NIL, 'SimpleNode'] = NIL) -> None:
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
                 left: Union[NIL, 'ComplexNode'] = NIL,
                 right: Union[NIL, 'ComplexNode'] = NIL) -> None:
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
    def __init__(self, root: Union[NIL, Node],
                 *,
                 key: Optional[SortingKey] = None) -> None:
        self._root = root
        self._key = key

    @property
    def root(self) -> Union[NIL, Node]:
        return self._root

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    def add(self, value: Domain) -> None:
        parent = self._root
        if parent is NIL:
            self._root = self._make_node(value)
            return
        key = self._to_key(value)
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    parent.left = self._make_node(value)
                    return
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    parent.right = self._make_node(value)
                    return
                else:
                    parent = parent.right
            else:
                return

    def discard(self, value: Domain) -> None:
        parent = self._root
        if parent is NIL:
            return
        key = self._to_key(value)
        if parent.key == key:
            if parent.left is NIL:
                self._root = parent.right
            else:
                node = parent.left
                if node.right is NIL:
                    self._root, node.right = node, self._root.right
                else:
                    while node.right.right is not NIL:
                        node = node.right
                    (self._root, node.right.left, node.right.right,
                     node.right) = (
                        node.right, self._root.left, self._root.right,
                        node.right.left)
            return
        while True:
            if key < parent.key:
                # search in left subtree
                if parent.left is NIL:
                    return
                elif parent.left.key == key:
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
                    parent = parent.left
            else:
                # search in right subtree
                if parent.right is NIL:
                    return
                elif parent.right.key == key:
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
                else:
                    parent = parent.right

    def popmax(self) -> Domain:
        node = self._root
        if node is NIL:
            raise KeyError
        elif node.right is NIL:
            self._root = node.left
            return node.value
        else:
            while node.right.right is not NIL:
                node = node.right
            result, node.right = node.right.value, node.right.left
            return result

    def popmin(self) -> Domain:
        node = self._root
        if node is NIL:
            raise KeyError
        elif node.left is NIL:
            self._root = node.right
            return node.value
        else:
            while node.left.left is not NIL:
                node = node.left
            result, node.left = node.left.value, node.left.right
            return result

    def clear(self) -> None:
        self._root = NIL

    def _make_node(self, value: Domain) -> Node:
        if self._key is None:
            return SimpleNode(value)
        else:
            return ComplexNode(self._key(value), value)

    @classmethod
    def from_iterable(cls, _values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'Tree[Domain]':
        values = list(_values)
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
                                  right=(to_node(middle_index + 1, end_index)
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
                                   right=(to_node(middle_index + 1, end_index)
                                          if middle_index < end_index - 1
                                          else NIL))

            root = to_node(0, len(items))
        return cls(root,
                   key=key)


def tree(*values: Domain, key: Optional[SortingKey] = None) -> Tree[Domain]:
    return Tree.from_iterable(values,
                              key=key)
