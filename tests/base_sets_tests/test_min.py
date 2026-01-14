import pytest
from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, set_value_to_key

from . import strategies


@given(strategies.empty_sets)
def test_base_case(set_: BaseSet[ValueT]) -> None:
    with pytest.raises(ValueError):
        set_.min()


@given(strategies.non_empty_sets)
def test_step(set_: BaseSet[ValueT]) -> None:
    result = set_.min()

    assert result in set_
    assert all(
        not set_value_to_key(set_, value) < set_value_to_key(set_, result)
        for value in set_
    )
