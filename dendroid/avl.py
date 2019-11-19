from abc import abstractmethod
from reprlib import recursive_repr
from typing import (Iterable,
                    Optional,
                    Union)

from reprit.base import generate_repr

from .binary import (NIL,
                     Node as _Node,
                     TreeBase,
                     _to_unique_sorted_items,
                     _to_unique_sorted_values)
from .hints import (Domain,
                    Sortable,
                    SortingKey)
from .utils import (_dereference_maybe,
                    _maybe_weakref)


class Node(_Node):
    @property
    @abstractmethod
    def height(self) -> int:
        """Height of the node."""

    parent = None  # type: Optional['Node']

    @property
    def balance_factor(self) -> int:
        return _to_height(self.left) - _to_height(self.right)


def _to_height(node: Union[NIL, Node]) -> int:
    return -1 if node is NIL else node.height


def _set_parent(node: Union[Node, NIL],
                parent: Optional[Node]) -> None:
    if node is not NIL:
        node.parent = parent


def _to_successor(node: Node) -> Union[Node, NIL]:
    if node.right is not NIL:
        node = node.right
        if node.left is NIL:
            return node
        else:
            while node.left.left is not NIL:
                node = node.left
            return node.left
    result = node.parent
    while result is not NIL and node is result.right:
        node, result = result, result.parent
    return result


class SimpleNode(Node):
    slots = ('_value', '_height', '_parent', '_left', '_right')

    def __init__(self, value: Domain,
                 *,
                 parent: Optional['SimpleNode'] = None,
                 left: Union['SimpleNode', NIL] = NIL,
                 right: Union['SimpleNode', NIL] = NIL) -> None:
        self._value = value
        self.parent = parent
        self._set_left(left)
        self._set_right(right)
        self._update_height()

    __repr__ = recursive_repr()(generate_repr(__init__))

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._value

    @property
    def height(self) -> int:
        return self._height

    @property
    def parent(self) -> Optional['SimpleNode']:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: Optional['SimpleNode']) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def left(self) -> Union['SimpleNode', NIL]:
        return self._left

    @left.setter
    def left(self, node: Union['SimpleNode', NIL]) -> None:
        self._set_left(node)
        self._update_height()

    @property
    def right(self) -> Union['SimpleNode', NIL]:
        return self._right

    @right.setter
    def right(self, node: Union['SimpleNode', NIL]) -> None:
        self._set_right(node)
        self._update_height()

    def _set_left(self, node: Union['SimpleNode', NIL]) -> None:
        self._left = node
        _set_parent(node, self)

    def _set_right(self, node: Union['SimpleNode', NIL]) -> None:
        self._right = node
        _set_parent(node, self)

    def _update_height(self) -> None:
        self._height = max(_to_height(self._left), _to_height(self._right)) + 1


class ComplexNode(Node):
    slots = ('_key', '_value', '_height', '_parent', 'left', 'right')

    def __init__(self, key: Sortable, value: Domain,
                 *,
                 parent: Optional['ComplexNode'] = None,
                 left: Union['ComplexNode', NIL] = NIL,
                 right: Union['ComplexNode', NIL] = NIL) -> None:
        self._value = value
        self._key = key
        self.parent = parent
        self._set_left(left)
        self._set_right(right)
        self._update_height()

    __repr__ = recursive_repr()(generate_repr(__init__))

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._key

    @property
    def height(self) -> int:
        return self._height

    @property
    def parent(self) -> Optional['ComplexNode']:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: Optional['ComplexNode']) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def left(self) -> Union['SimpleNode', NIL]:
        return self._left

    @left.setter
    def left(self, node: Union['SimpleNode', NIL]) -> None:
        self._set_left(node)
        self._update_height()

    @property
    def right(self) -> Union['SimpleNode', NIL]:
        return self._right

    @right.setter
    def right(self, node: Union['SimpleNode', NIL]) -> None:
        self._set_right(node)
        self._update_height()

    def _set_left(self, node: Union['SimpleNode', NIL]) -> None:
        self._left = node
        _set_parent(node, self)

    def _set_right(self, node: Union['SimpleNode', NIL]) -> None:
        self._right = node
        _set_parent(node, self)

    def _update_height(self) -> None:
        self._height = max(_to_height(self._left), _to_height(self._right)) + 1


class Tree(TreeBase[Domain]):
    def __init__(self, root: Union[Node, NIL],
                 *,
                 key: Optional[SortingKey] = None) -> None:
        self._root = root
        self._key = key

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def root(self) -> Optional[Node]:
        return self._root

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

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

    def __contains__(self, value: Domain) -> bool:
        return self._search_node(value) is not NIL

    def add(self, value: Domain) -> None:
        parent = self._root
        if parent is NIL:
            self._root = self._make_node(value)
            return
        key = self._to_key(value)
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    node = self._make_node(value)
                    parent.left = node
                    break
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    node = self._make_node(value)
                    parent.right = node
                    break
                else:
                    parent = parent.right
            else:
                return
        self._restore(node.parent)

    def discard(self, value: Domain) -> None:
        node = self._search_node(value)
        if node is NIL:
            return
        self._remove_node(node)

    def popmax(self) -> Domain:
        node = self.root
        if node is None:
            raise KeyError
        while node.right is not NIL:
            node = node.right
        self._remove_node(node)
        return node.value

    def popmin(self) -> Domain:
        node = self.root
        if node is None:
            raise KeyError
        while node.left is not NIL:
            node = node.left
        self._remove_node(node)
        return node.value

    def clear(self) -> None:
        self._root = None

    def _make_node(self, value: Domain) -> Node:
        if self._key is None:
            return SimpleNode(value)
        else:
            return ComplexNode(self._key(value), value)

    def _search_node(self, value: Domain) -> Optional[Node]:
        result = self._root
        key = self._to_key(value)
        while result is not NIL:
            if key < result.key:
                result = result.left
            elif result.key < key:
                result = result.right
            else:
                break
        return result

    def _remove_node(self, node: Node) -> None:
        if node.left is NIL:
            imbalanced_node = node.parent
            self._transplant(node, node.right)
        elif node.right is NIL:
            imbalanced_node = node.parent
            self._transplant(node, node.left)
        else:
            successor = _to_successor(node)
            if successor.parent is node:
                imbalanced_node = successor
            else:
                imbalanced_node = successor.parent
                self._transplant(successor, successor.right)
                successor.right = node.right
            self._transplant(node, successor)
            successor.left, successor.left.parent = node.left, successor
        self._remove_node_fixup(imbalanced_node)

    def _restore(self, node: Optional[Node]) -> None:
        while node is not None and node.balance_factor:
            if node.balance_factor > 1 or node.balance_factor < -1:
                self._rebalance(node)
                return
            node = node.parent

    def _remove_node_fixup(self, node: Node) -> None:
        while node is not None:
            self._rebalance(node)
            node = node.parent

    def _rebalance(self, node: Node) -> None:
        if node.balance_factor > 1:
            if node.left.balance_factor < 0:
                self._rotate_left(node.left)
            self._rotate_right(node)
        elif node.balance_factor < -1:
            if node.right.balance_factor > 0:
                self._rotate_right(node.right)
            self._rotate_left(node)

    def _rotate_right(self, node: Node) -> None:
        parent, replacement = node.parent, node.left
        if parent is None:
            replacement.parent, self._root = None, replacement
        elif node is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement
        replacement.right, node.left = node, replacement.right

    def _rotate_left(self, node: Node) -> None:
        parent, replacement = node.parent, node.right
        if parent is None:
            replacement.parent, self._root = None, replacement
        elif parent.left is node:
            parent.left = replacement
        else:
            parent.right = replacement
        replacement.left, node.right = node, replacement.left

    def _transplant(self, origin: Node, replacement: Optional[Node]) -> None:
        parent = origin.parent
        if parent is None:
            self._root = replacement
        elif origin is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement
        _set_parent(replacement, parent)

    def _to_key(self, value: Domain) -> Sortable:
        return value if self._key is None else self._key(value)


def tree(*values: Domain, key: Optional[SortingKey] = None) -> Tree[Domain]:
    return Tree.from_iterable(values,
                              key=key)
