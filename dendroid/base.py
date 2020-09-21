import sys
from abc import (ABC,
                 abstractmethod)
from itertools import chain
from typing import (Generic,
                    Iterable,
                    Iterator,
                    MutableSet,
                    Optional,
                    Sequence,
                    Union)

from reprit.base import generate_repr

from .hints import (Domain,
                    OtherDomain,
                    Sortable,
                    SortingKey)
from .utils import capacity

NIL = None


class Node(ABC):
    left = NIL  # type: Union[NIL, 'Node']
    right = NIL  # type: Union[NIL, 'Node']

    @property
    @abstractmethod
    def value(self) -> Domain:
        """Contained value."""

    @property
    @abstractmethod
    def key(self) -> Sortable:
        """Comparisons key."""


@MutableSet.register
class TreeBase(ABC, Generic[Domain]):
    @property
    @abstractmethod
    def root(self) -> Union[NIL, Node]:
        """Root node."""

    @property
    @abstractmethod
    def key(self) -> Optional[SortingKey]:
        """Sorting key."""

    @classmethod
    @abstractmethod
    def from_iterable(cls, _values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'TreeBase[Domain]':
        """Constructs tree from given iterable using given sorting key."""

    @property
    def _values(self) -> Sequence[Domain]:
        return list(self)

    __repr__ = generate_repr(from_iterable,
                             with_module_name=True)

    if sys.version_info < (3, 6, 4):
        # caused by https://github.com/python/typing/issues/498

        def __copy__(self) -> 'TreeBase[Domain]':
            return self.from_iterable(self,
                                      key=self.key)

    def __bool__(self) -> bool:
        """Checks if the tree has nodes."""
        return self.root is not NIL

    def __len__(self) -> int:
        """Returns number of nodes."""
        return capacity(self)

    def __iter__(self) -> Iterator[Domain]:
        """Returns iterator over values in ascending keys order."""
        node = self.root
        queue = []
        while True:
            while node is not NIL:
                queue.append(node)
                node = node.left
            if not queue:
                return
            node = queue.pop()
            yield node.value
            node = node.right

    def __reversed__(self) -> Iterator[Domain]:
        """Returns iterator over values in descending keys order."""
        node = self.root
        queue = []
        while True:
            while node is not NIL:
                queue.append(node)
                node = node.right
            if not queue:
                return
            node = queue.pop()
            yield node.value
            node = node.left

    def __contains__(self, value: Domain) -> bool:
        """Checks if given value is contained in the tree."""
        try:
            self._search_node(value)
        except ValueError:
            return False
        else:
            return True

    def __eq__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is equal to given one."""
        return (len(self) == len(other) and self <= other <= self
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __le__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a subset of given one."""
        return (len(self) <= len(other)
                and all(value in other for value in self)
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __lt__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a strict subset of given one."""
        return (len(self) < len(other)
                and self <= other and self != other
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __gt__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a strict superset of given one."""
        return (len(self) > len(other)
                and self >= other and self != other
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __ge__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a superset of given one."""
        return (len(self) >= len(other)
                and all(value in self for value in other)
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __and__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Returns intersection of the tree with given one."""
        return (self.from_iterable((value for value in self if value in other),
                                   key=self.key)
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __or__(self, other: 'TreeBase[OtherDomain]'
               ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Returns union of the tree with given one."""
        return (self.from_iterable(chain(self, other),
                                   key=self.key)
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __sub__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Returns subtraction of the tree with given one."""
        return (self.from_iterable((value
                                    for value in self
                                    if value not in other),
                                   key=self.key)
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __xor__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Returns symmetric difference of the tree with given one."""
        return ((self - other) | (other - self)
                if isinstance(other, TreeBase)
                else NotImplemented)

    def __iand__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Intersects the tree with given one in-place."""
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

    def __isub__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Subtracts from the tree a given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                self.discard(value)
        return self

    def max(self) -> Domain:
        """Returns maximum value from the tree."""
        node = self.root
        if node is NIL:
            raise ValueError('Tree is empty.')
        while node.right is not NIL:
            node = node.right
        return node.value

    def min(self) -> Domain:
        """Returns minimum value from the tree."""
        node = self.root
        if node is NIL:
            raise ValueError('Tree is empty.')
        while node.left is not NIL:
            node = node.left
        return node.value

    def next(self, value: Domain) -> Domain:
        """Returns first value with a key greater than of the given value."""
        return self._to_successor(self._search_node(value)).value

    def prev(self, value: Domain) -> Domain:
        """Returns last value with a key less than of the given value."""
        return self._to_predecessor(self._search_node(value)).value

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
        """Removes given value from the tree if it exists."""

    def pop(self) -> Domain:
        """Pops value from the tree."""
        iterator = iter(self)
        try:
            result = next(iterator)
        except StopIteration:
            raise KeyError
        self.discard(result)
        return result

    @abstractmethod
    def popmax(self) -> Domain:
        """Pops maximum value from the tree."""

    @abstractmethod
    def popmin(self) -> Domain:
        """Pops minimum value from the tree."""

    @abstractmethod
    def clear(self) -> None:
        """Clears the tree."""

    def isdisjoint(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree has no intersection with given one."""
        return (all(value not in other for value in self)
                if len(self) < len(other)
                else all(value not in self for value in other))

    def _to_key(self, value: Domain) -> Sortable:
        return value if self.key is None else self.key(value)

    def _search_node(self, value: Domain) -> Node:
        node = self._root
        if node is NIL:
            raise ValueError('Tree is empty.')
        key = self._to_key(value)
        while node is not NIL:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                return node
        raise ValueError('Value is not in tree.')

    def _to_successor(self, node: Node) -> Node:
        if node.right is NIL:
            candidate, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                if key < cursor.key:
                    candidate, cursor = cursor, cursor.left
                else:
                    cursor = cursor.right
            if candidate is NIL:
                raise ValueError('Corresponds to a maximum node.')
            else:
                return candidate
        else:
            result = node.right
            while result.left is not NIL:
                result = result.left
            return result

    def _to_predecessor(self, node: Node) -> Node:
        if node.left is NIL:
            candidate, cursor, key = NIL, self.root, node.key
            while cursor is not node:
                if key > cursor.key:
                    candidate, cursor = cursor, cursor.right
                else:
                    cursor = cursor.left
            if candidate is NIL:
                raise ValueError('Corresponds to a minimum node.')
            else:
                return candidate
        else:
            result = node.left
            while result.right is not NIL:
                result = result.right
            return result
