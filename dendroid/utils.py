import weakref
from typing import Optional

from .hints import Domain

to_balanced_tree_height = int.bit_length


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
