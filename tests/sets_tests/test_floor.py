from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import Value
from tests.utils import (BaseSet,
                         set_value_to_key)
from . import strategies


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.floor(value)


@given(strategies.non_empty_sets_with_values)
def test_step(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    key = set_value_to_key(set_, value)
    try:
        floor = set_.floor(value)
    except ValueError:
        assert key < set_value_to_key(set_, set_.min())
    else:
        floor_key = set_value_to_key(set_, floor)
        assert (not key < floor_key
                and all(key < set_value_to_key(set_, element)
                        or not floor_key < set_value_to_key(set_, element)
                        for element in set_))


@given(strategies.non_empty_sets)
def test_elements(set_: BaseSet) -> None:
    assert all(set_.floor(element) is element for element in set_)
