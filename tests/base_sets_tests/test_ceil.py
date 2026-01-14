import pytest
from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, set_value_to_key

from . import strategies


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.ceil(value)


@given(strategies.non_empty_sets_with_values)
def test_step(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    key = set_value_to_key(set_, value)
    try:
        ceil = set_.ceil(value)
    except ValueError:
        assert set_value_to_key(set_, set_.max()) < key
    else:
        ceil_key = set_value_to_key(set_, ceil)
        assert not ceil_key < key
        assert all(
            set_value_to_key(set_, element) < key
            or not set_value_to_key(set_, element) < ceil_key
            for element in set_
        )


@given(strategies.non_empty_sets)
def test_elements(set_: BaseSet[ValueT]) -> None:
    assert all(set_.ceil(element) is element for element in set_)
