from hypothesis import given
from lz.iterating import (capacity,
                          pairwise)

from tests.utils import (Set,
                         value_to_key)
from . import strategies


@given(strategies.sets)
def test_size(set_: Set) -> None:
    result = reversed(set_)

    assert capacity(result) == len(set_)


@given(strategies.sets)
def test_elements(set_: Set) -> None:
    result = reversed(set_)

    assert all(value in set_ for value in result)


@given(strategies.sets_with_two_or_more_nodes)
def test_order(set_: Set) -> None:
    result = reversed(set_)

    assert all(value_to_key(set_, value) > value_to_key(set_, next_value)
               for value, next_value in pairwise(result))
