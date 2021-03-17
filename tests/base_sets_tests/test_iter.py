from hypothesis import given

from tests.utils import (BaseSet,
                         capacity,
                         pairwise,
                         set_value_to_key)
from . import strategies


@given(strategies.sets)
def test_size(set_: BaseSet) -> None:
    result = iter(set_)

    assert capacity(result) == len(set_)


@given(strategies.sets)
def test_elements(set_: BaseSet) -> None:
    result = iter(set_)

    assert all(element in set_ for element in result)


@given(strategies.sets_with_two_or_more_values)
def test_order(set_: BaseSet) -> None:
    result = iter(set_)

    assert all(set_value_to_key(set_, value)
               < set_value_to_key(set_, next_value)
               for value, next_value in pairwise(result))
