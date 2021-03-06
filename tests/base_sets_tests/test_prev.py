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
        set_.prev(value)


@given(strategies.non_empty_sets_with_their_values)
def test_step(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    assert (value == set_.min()
            or set_value_to_key(set_, set_.prev(value))
            < set_value_to_key(set_, value))


@given(strategies.non_empty_sets_with_external_values)
def test_external_value(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.prev(value)


@given(strategies.non_empty_sets)
def test_minimum(set_: BaseSet) -> None:
    minimum = set_.min()

    with pytest.raises(ValueError):
        set_.prev(minimum)
