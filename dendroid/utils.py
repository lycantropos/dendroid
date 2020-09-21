import weakref
from collections import deque
from itertools import count
from typing import (Any,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    Tuple)

from .hints import (Domain,
                    Sortable,
                    SortingKey)


def to_balanced_tree_height(size: int) -> int:
    return size.bit_length() - 1


def _maybe_weakref(object_: Optional[Domain]
                   ) -> Optional[weakref.ReferenceType]:
    return (object_
            if object_ is None
            else weakref.ref(object_))


def _dereference_maybe(maybe_reference: Optional[weakref.ref]
                       ) -> Optional[Domain]:
    return (maybe_reference
            if maybe_reference is None
            else maybe_reference())


def capacity(iterable: Iterable[Any]) -> int:
    """
    Returns number of elements in iterable.

    >>> capacity(range(0))
    0
    >>> capacity(range(10))
    10
    """
    counter = count()
    # order matters: if `counter` goes first,
    # then it will be incremented even for empty `iterable`
    deque(zip(iterable, counter),
          maxlen=0)
    return next(counter)


def _to_unique_sorted_items(values: Sequence[Domain], sorting_key: SortingKey
                            ) -> Sequence[Tuple[Sortable, Domain]]:
    keys_indices = []  # type: List[Tuple[Sortable, int]]
    for key, index in sorted((sorting_key(value), index)
                             for index, value in enumerate(values)):
        while keys_indices and keys_indices[-1][0] == key:
            del keys_indices[-1]
        keys_indices.append((key, index))
    return [(key, values[index]) for key, index in keys_indices]


def _to_unique_sorted_values(values: Sequence[Domain]) -> Sequence[Domain]:
    result = []  # type: List[Domain]
    for value in sorted(values):
        while result and result[-1] == value:
            del result[-1]
        result.append(value)
    return result
