from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         value_to_key)
from . import strategies


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.next(value)


@given(strategies.non_empty_sets_with_their_values)
def test_step(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    assert (value == set_.max()
            or (value_to_key(set_, value)
                < value_to_key(set_, set_.next(value))))


@given(strategies.non_empty_sets_with_external_values)
def test_external_value(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.next(value)


@given(strategies.non_empty_sets)
def test_maximum(set_: Set) -> None:
    maximum = set_.max()

    with pytest.raises(ValueError):
        set_.next(maximum)
