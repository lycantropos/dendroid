from abc import (ABC,
                 abstractmethod)
from collections import deque
from itertools import chain
from typing import (Generic,
                    Iterable,
                    Iterator,
                    MutableSet,
                    Optional,
                    Sequence,
                    Tuple,
                    Union)

from lz.iterating import capacity
from reprit.base import generate_repr

from .hints import (Domain,
                    OtherDomain,
                    Sortable,
                    SortingKey)


class Node(ABC):
    left = None  # type: Optional['_Node']
    right = None  # type: Optional['_Node']

    @property
    @abstractmethod
    def value(self) -> Domain:
        pass

    @property
    @abstractmethod
    def key(self) -> Sortable:
        pass


class SimpleNode(Node):
    __slots__ = ('_value', 'left', 'right')

    def __init__(self, value: Domain,
                 *,
                 left: Optional[Node] = None,
                 right: Optional[Node] = None) -> None:
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
    __slots__ = ('_value', '_key', 'left', 'right')

    def __init__(self, value: Domain, key: Sortable,
                 *,
                 left: Optional['ComplexNode'] = None,
                 right: Optional['ComplexNode'] = None) -> None:
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


@MutableSet.register
class TreeBase(ABC, Generic[Domain]):
    @property
    @abstractmethod
    def root(self) -> Optional[Node]:
        """Root node."""

    @property
    @abstractmethod
    def key(self) -> Optional[SortingKey]:
        """Sorting key."""

    @classmethod
    @abstractmethod
    def from_iterable(cls, values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'TreeBase[Domain]':
        """Constructs tree from given iterable using given sorting key."""

    def __len__(self) -> int:
        """Returns number of nodes."""
        return capacity(iter(self))

    def __iter__(self) -> Iterator[Domain]:
        """Returns iterator over values."""
        if self.root is None:
            return
        queue = deque([self.root])
        while queue:
            node = queue.pop()
            yield node.value
            if node.left is not None:
                queue.appendleft(node.left)
            if node.right is not None:
                queue.appendleft(node.right)

    @abstractmethod
    def __contains__(self, value: Domain) -> bool:
        """Checks if given value is contained in the tree."""

    def __eq__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is equal to given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return len(self) == len(other) and self <= other <= self

    def __le__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a subset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return all(value in other for value in self)

    def __lt__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a strict subset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self <= other and self != other

    def __gt__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a strict superset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self >= other and self != other

    def __ge__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a superset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return all(value in self for value in other)

    def __and__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Domain]':
        """Returns intersection of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self.from_iterable((value for value in self if value in other),
                                  key=self.key)

    def __or__(self, other: 'TreeBase[OtherDomain]'
               ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Returns union of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self.from_iterable(chain(self, other),
                                  key=self.key)

    def __sub__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Domain]':
        """Returns subtraction of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self.from_iterable((value
                                   for value in self
                                   if value not in other),
                                  key=self.key)

    def __xor__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Returns symmetric difference of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return (self - other) | (other - self)

    def __iand__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Intersects tree with given objects in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        for value in self - other:
            self.discard(value)
        return self

    def __ior__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Unites the tree with given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        for value in other:
            self.add(value)
        return self

    def __ixor__(self, other: 'TreeBase[OtherDomain]'
                 ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Exclusively disjoins the tree with given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                if value in self:
                    self.discard(value)
                else:
                    self.add(value)
        return self

    def __isub__(self, other: 'TreeBase[OtherDomain]'
                 ) -> 'TreeBase[Domain]':
        """Subtracts the tree with given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                self.discard(value)
        return self

    @abstractmethod
    def add(self, value: Domain) -> None:
        """Adds given value to the tree."""

    def remove(self, value: Domain) -> None:
        """Removes given value from the tree."""
        if value not in self:
            raise KeyError(value)
        self.discard(value)

    @abstractmethod
    def discard(self, value: Domain) -> None:
        """Removes given value from tree if it exists."""

    def pop(self) -> Domain:
        """Pops value from tree."""
        iterator = iter(self)
        try:
            result = next(iterator)
        except StopIteration:
            raise KeyError
        self.discard(result)
        return result

    @abstractmethod
    def clear(self) -> None:
        """Clears the tree."""

    def isdisjoint(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree has no intersection with given one."""

        def _are_disjoint(left: TreeBase[Domain],
                          right: TreeBase[OtherDomain]) -> bool:
            for value in left:
                if value in right:
                    return False
            return True

        return (_are_disjoint(self, other)
                if len(self) < len(other)
                else _are_disjoint(other, self))


class Tree(TreeBase[Domain]):
    def __init__(self, root: Node,
                 *,
                 key: Optional[SortingKey] = None) -> None:
        self._root = root
        self._key = key

    __repr__ = generate_repr(__init__)

    @property
    def root(self) -> Optional[Node]:
        return self._root

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    def __contains__(self, value: Domain) -> bool:
        node = self._root
        if node is None:
            return False
        key = self._to_key(value)
        while node is not None:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                return node.key == key
        return False

    def add(self, value: Domain) -> None:
        parent = self._root
        if parent is None:
            self._root = self._make_node(value)
            return
        key = self._to_key(value)
        while True:
            if key < parent.key:
                if parent.left is None:
                    parent.left = self._make_node(value)
                    return
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is None:
                    parent.right = self._make_node(value)
                    return
                else:
                    parent = parent.right
            else:
                return

    def discard(self, value: Domain) -> None:
        parent = self._root
        if parent is None:
            return
        key = self._to_key(value)
        if parent.key == key:
            if parent.left is None:
                self._root = parent.right
            else:
                node = parent.left
                if node.right is None:
                    self._root, node.right = node, self._root.right
                else:
                    while node.right.right is not None:
                        node = node.right
                    (self._root, node.right.left, node.right.right,
                     node.right) = (
                        node.right, self._root.left, self._root.right,
                        node.right.left)
            return
        while True:
            if key < parent.key:
                # search in left subtree
                if parent.left is None:
                    return
                elif key < parent.left.key or parent.left.key < key:
                    parent = parent.left
                elif parent.left.key == key:
                    # remove `parent.left`
                    node = parent.left.left
                    if node is None:
                        parent.left = parent.left.right
                        return
                    elif node.right is None:
                        parent.left, node.right = node, parent.left.right
                    else:
                        while node.right.right is not None:
                            node = node.right
                        (parent.left, node.right.left, node.right.right,
                         node.right) = (
                            node.right, parent.left.left, parent.left.right,
                            node.right.left)
                else:
                    return
            else:
                # search in right subtree
                if parent.right is None:
                    return
                elif key < parent.right.key or parent.right.key < key:
                    parent = parent.right
                elif parent.right.key == key:
                    # remove `parent.right`
                    node = parent.right.left
                    if node is None:
                        parent.right = parent.right.right
                        return
                    elif node.right is None:
                        parent.right, node.right = node, parent.right.right
                    else:
                        while node.right.right is not None:
                            node = node.right
                        (parent.right, node.right.left, node.right.right,
                         node.right) = (
                            node.right, parent.right.left, parent.right.right,
                            node.right.left)
                else:
                    return

    def clear(self) -> None:
        self._root = None

    def _make_node(self, value: Domain) -> Node:
        if self._key is None:
            return SimpleNode(value)
        else:
            return ComplexNode(value, self._key(value))

    def _to_key(self, value: Domain) -> Sortable:
        return value if self._key is None else self._key(value)

    @classmethod
    def from_iterable(cls, values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'Tree[Domain]':
        values = list(values)
        if not values:
            root = None
        elif key is None:
            def to_node(sub_values: Sequence[Domain]) -> SimpleNode:
                midpoint = len(sub_values) // 2
                left = (to_node(sub_values[:midpoint])
                        if midpoint > 0
                        else None)
                right = (to_node(sub_values[midpoint + 1:])
                         if midpoint < len(sub_values) - 1
                         else None)
                return SimpleNode(sub_values[midpoint],
                                  left=left,
                                  right=right)

            root = to_node(_to_unique_sorted_values(values))
        else:
            def to_node(sub_keys_values: Sequence[Tuple[Domain, Sortable]]
                        ) -> ComplexNode:
                midpoint = len(sub_keys_values) // 2
                return ComplexNode(*sub_keys_values[midpoint],
                                   left=(to_node(sub_keys_values[:midpoint])
                                         if midpoint > 0
                                         else None),
                                   right=(
                                       to_node(sub_keys_values[midpoint + 1:])
                                       if midpoint < len(sub_keys_values) - 1
                                       else None))

            root = to_node(_to_unique_keys_values(values, key))
        return cls(root,
                   key=key)


def tree(*values: Domain, key: Optional[SortingKey] = None) -> Tree[Domain]:
    return Tree.from_iterable(values,
                              key=key)


def _to_unique_keys_values(values: Sequence[Domain], sorting_key: SortingKey
                           ) -> Sequence[Tuple[Domain, Sortable]]:
    keys_indices = []
    for key, index in sorted([(sorting_key(value), index)
                              for index, value in enumerate(values)],
                             key=sorting_key):
        while keys_indices and keys_indices[-1][0] == key:
            del keys_indices[-1]
        keys_indices.append((key, index))
    return [(values[index], key) for key, index in keys_indices]


def _to_unique_sorted_values(values: Sequence[Domain]) -> Sequence[Domain]:
    result = []
    for value in sorted(values):
        while result and result[-1] == value:
            del result[-1]
        result.append(value)
    return result
