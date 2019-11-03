import weakref
from reprlib import recursive_repr
from typing import (Iterable,
                    Optional,
                    Union)

from reprit.base import generate_repr

from dendroid.hints import (Domain,
                            Sortable,
                            SortingKey)
from .binary import (Node as _Node,
                     TreeBase)

LeafNode = type(None)
NIL = None


class InnerNode(_Node):
    left = NIL  # type: Union['InnerNode', LeafNode]
    right = NIL  # type: Union['InnerNode', LeafNode]
    parent = None  # type: Optional['InnerNode']
    is_black = False  # type: bool


def _maybe_weakref(object_: Optional[Domain]
                   ) -> Optional[weakref.ReferenceType]:
    return object_ if object_ is None else weakref.ref(object_)


def _dereference_maybe(maybe_reference: Optional[weakref.ref]
                       ) -> Optional[Domain]:
    return (maybe_reference
            if maybe_reference is None
            else maybe_reference())


class SimpleInnerNode(InnerNode):
    slots = ('_value', 'is_black', '_parent', '_left', '_right')

    def __init__(self, value: Domain,
                 *,
                 is_black: bool,
                 parent: Optional['SimpleInnerNode'] = None,
                 left: Union['SimpleInnerNode', LeafNode] = NIL,
                 right: Union['SimpleInnerNode', LeafNode] = NIL) -> None:
        self._value = value
        self.is_black = is_black
        self._parent = _maybe_weakref(parent)
        self._left = left
        self._right = right

    __repr__ = recursive_repr()(generate_repr(__init__))

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._value

    @property
    def parent(self) -> Optional['SimpleInnerNode']:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: Optional['SimpleInnerNode']) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def left(self) -> Union['SimpleInnerNode', LeafNode]:
        return self._left

    @left.setter
    def left(self, node: Union['SimpleInnerNode', LeafNode]) -> None:
        self._left = node
        _set_parent(node, self)

    @property
    def right(self) -> Union['SimpleInnerNode', LeafNode]:
        return self._right

    @right.setter
    def right(self, node: Union['SimpleInnerNode', LeafNode]) -> None:
        self._right = node
        _set_parent(node, self)


class ComplexInnerNode(InnerNode):
    slots = ('_value', '_key', 'is_black', '_parent', 'left', 'right')

    def __init__(self, value: Domain, key: Sortable,
                 *,
                 is_black: bool,
                 parent: Optional['ComplexInnerNode'] = None,
                 left: Union['ComplexInnerNode', LeafNode] = NIL,
                 right: Union['ComplexInnerNode', LeafNode] = NIL) -> None:
        self._value = value
        self._key = key
        self.is_black = is_black
        self._parent = _maybe_weakref(parent)
        self.left = left
        self.right = right

    __repr__ = recursive_repr()(generate_repr(__init__))

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._key

    @property
    def parent(self) -> Optional['ComplexInnerNode']:
        return _dereference_maybe(self._parent)

    @parent.setter
    def parent(self, node: Optional['ComplexInnerNode']) -> None:
        self._parent = _maybe_weakref(node)

    @property
    def left(self) -> Union['ComplexInnerNode', LeafNode]:
        return self._left

    @left.setter
    def left(self, node: Union['ComplexInnerNode', LeafNode]) -> None:
        self._left = node
        _set_parent(node, self)

    @property
    def right(self) -> Union['ComplexInnerNode', LeafNode]:
        return self._right

    @right.setter
    def right(self, node: Union['ComplexInnerNode', LeafNode]) -> None:
        self._right = node
        _set_parent(node, self)


def _set_parent(node: Union[InnerNode, LeafNode],
                parent: Optional[InnerNode]) -> None:
    if _is_inner_node(node):
        node.parent = parent


def _set_black(maybe_node: Optional[InnerNode]) -> None:
    if maybe_node is not None:
        maybe_node.is_black = True


def _is_left_child(node: InnerNode) -> bool:
    parent = node.parent
    return parent is not None and parent.left is node


def _is_inner_node(node: Union[InnerNode, LeafNode]) -> bool:
    return node is not NIL


def _is_leaf_node(node: Union[InnerNode, LeafNode]) -> bool:
    return node is NIL


def _to_successor(node: InnerNode) -> Union[InnerNode, LeafNode]:
    if _is_inner_node(node.right):
        node = node.right
        if _is_leaf_node(node.left):
            return node
        else:
            while _is_inner_node(node.left.left):
                node = node.left
            return node.left
    result = node.parent
    while _is_inner_node(result) and node is result.right:
        node, result = result, result.parent
    return result


def _is_node_black(node: Union[InnerNode, LeafNode]) -> bool:
    return _is_leaf_node(node) or node.is_black


class Tree(TreeBase[Domain]):
    def __init__(self, root: Union[InnerNode, LeafNode],
                 *,
                 key: Optional[SortingKey] = None) -> None:
        self._root = root
        self._key = key

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def root(self) -> Optional[InnerNode]:
        return self._root

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    @classmethod
    def from_iterable(cls, values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'Tree[Domain]':
        result = cls(NIL,
                     key=key)
        for value in values:
            result.add(value)
        return result

    def __contains__(self, value: Domain) -> bool:
        node = self._search_node(value)
        return not _is_leaf_node(node)

    def add(self, value: Domain) -> None:
        parent = self._root
        if _is_leaf_node(parent):
            self._root = self._make_node(value,
                                         is_black=True)
            return
        key = self._to_key(value)
        while True:
            if key < parent.key:
                if _is_leaf_node(parent.left):
                    node = self._make_node(value,
                                           is_black=False)
                    parent.left = node
                    break
                else:
                    parent = parent.left
            elif parent.key < key:
                if _is_leaf_node(parent.right):
                    node = self._make_node(value,
                                           is_black=False)
                    parent.right = node
                    break
                else:
                    parent = parent.right
            else:
                return
        self._restore(node)

    def discard(self, value: Domain) -> None:
        node = self._search_node(value)
        if _is_leaf_node(node):
            return
        self._remove_node(node)

    def popmax(self) -> Domain:
        node = self.root
        if node is None:
            raise KeyError
        while _is_inner_node(node.right):
            node = node.right
        self._remove_node(node)
        return node.value

    def popmin(self) -> Domain:
        node = self.root
        if node is None:
            raise KeyError
        while _is_inner_node(node.left):
            node = node.left
        self._remove_node(node)
        return node.value

    def clear(self) -> None:
        self._root = None

    def _make_node(self, value: Domain,
                   *,
                   is_black: bool) -> InnerNode:
        if self._key is None:
            return SimpleInnerNode(value,
                                   is_black=is_black)
        else:
            return ComplexInnerNode(value, self._key(value),
                                    is_black=is_black)

    def _search_node(self, value: Domain) -> Optional[InnerNode]:
        node = self._root
        key = self._to_key(value)
        while _is_inner_node(node):
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                break
        return node

    def _restore(self, node: InnerNode) -> None:
        while not _is_node_black(node.parent):
            parent = node.parent
            grandparent = parent.parent
            if parent is grandparent.left:
                # uncle is on the right
                uncle = grandparent.right
                if _is_node_black(uncle):
                    # uncle is black
                    if node is parent.right:
                        self._rotate_left(parent)
                        node, parent = parent, node
                    parent.is_black = True
                    grandparent.is_black = False
                    self._rotate_right(grandparent)
                else:
                    # uncle is red
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
            else:
                # uncle is on the left
                uncle = grandparent.left
                if _is_node_black(uncle):
                    # uncle is black
                    if node is parent.left:
                        self._rotate_right(parent)
                        node, parent = parent, node
                    parent.is_black = True
                    grandparent.is_black = False
                    self._rotate_left(grandparent)
                else:
                    # uncle is red
                    parent.is_black = uncle.is_black = True
                    grandparent.is_black = False
                    node = grandparent
        self._root.is_black = True

    def _remove_node(self, node: InnerNode) -> None:
        successor, is_node_black = node, node.is_black
        if _is_leaf_node(successor.left):
            (successor_child, successor_child_parent,
             is_successor_child_left) = (successor.right, successor.parent,
                                         _is_left_child(successor))
            self._transplant(successor, successor_child)
        elif _is_leaf_node(successor.right):
            (successor_child, successor_child_parent,
             is_successor_child_left) = (successor.left, successor.parent,
                                         _is_left_child(successor))
            self._transplant(successor, successor_child)
        else:
            successor = _to_successor(node)
            is_node_black = successor.is_black
            successor_child, is_successor_child_left = successor.right, False
            if successor.parent == node:
                _set_parent(successor_child, successor)
                successor_child_parent = successor
            else:
                is_successor_child_left = _is_left_child(successor)
                successor_child_parent = successor.parent
                self._transplant(successor, successor.right)
                successor.right = node.right
                _set_parent(successor.right, successor)
            self._transplant(node, successor)
            successor.left, successor.left.parent = node.left, successor
            successor.is_black = node.is_black
        if is_node_black:
            self._remove_node_fixup(successor_child, successor_child_parent,
                                    is_successor_child_left)

    def _remove_node_fixup(self, node: Union[InnerNode, LeafNode],
                           parent: InnerNode, is_left_child: bool) -> None:
        while node is not self._root and _is_node_black(node):
            if is_left_child:
                sibling = parent.right
                if not _is_node_black(sibling):
                    sibling.is_black = True
                    parent.is_black = False
                    self._rotate_left(parent)
                    sibling = parent.right
                if (_is_node_black(sibling.left)
                        and _is_node_black(sibling.right)):
                    sibling.is_black = False
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.right):
                        sibling.left.is_black = True
                        sibling.is_black = False
                        self._rotate_right(sibling)
                        sibling = parent.right
                    sibling.is_black = parent.is_black
                    parent.is_black = True
                    _set_black(sibling.right)
                    self._rotate_left(parent)
                    node = self._root
            else:
                sibling = parent.left
                if not _is_node_black(sibling):
                    sibling.is_black = True
                    parent.is_black = False
                    self._rotate_right(parent)
                    sibling = parent.left
                if (_is_node_black(sibling.left)
                        and _is_node_black(sibling.right)):
                    sibling.is_black = False
                    node, parent = parent, parent.parent
                    is_left_child = _is_left_child(node)
                else:
                    if _is_node_black(sibling.left):
                        sibling.right.is_black = True
                        sibling.is_black = False
                        self._rotate_left(sibling)
                        sibling = parent.left
                    sibling.is_black = parent.is_black
                    parent.is_black = True
                    _set_black(sibling.left)
                    self._rotate_right(parent)
                    node = self._root
        _set_black(node)

    def _transplant(self, origin: InnerNode,
                    replacement: Optional[InnerNode]) -> None:
        if origin.parent is None:
            self._root = replacement
        elif origin.parent.left is origin:
            origin.parent.left = replacement
        else:
            origin.parent.right = replacement
        _set_parent(replacement, origin.parent)

    def _rotate_right(self, node: InnerNode) -> None:
        replacement = node.left
        parent = node.parent
        replacement.right, node.left = node, replacement.right
        if parent is None:
            replacement.parent = None
            self._root = replacement
        elif node is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement

    def _rotate_left(self, node: InnerNode) -> None:
        replacement = node.right
        parent = node.parent
        replacement.left, node.right = node, replacement.left
        if parent is None:
            replacement.parent = None
            self._root = replacement
        elif parent.left is node:
            parent.left = replacement
        else:
            parent.right = replacement

    def _to_key(self, value: Domain) -> Sortable:
        return value if self._key is None else self._key(value)


def tree(*values: Domain, key: Optional[SortingKey] = None) -> Tree[Domain]:
    return Tree.from_iterable(values,
                              key=key)
