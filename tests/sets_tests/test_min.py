import pytest
from hypothesis import given

from tests.utils import (Set,
                         value_to_key)
from . import strategies


@given(strategies.empty_sets)
def test_base_case(set_: Set) -> None:
    with pytest.raises(ValueError):
        set_.min()


@given(strategies.non_empty_sets)
def test_step(set_: Set) -> None:
    result = set_.min()

    assert result in set_
    assert all(not value_to_key(set_, value) < value_to_key(set_, result)
               for value in set_)
