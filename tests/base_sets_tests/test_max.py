import pytest
from hypothesis import given

from tests.utils import (BaseSet,
                         set_value_to_key)
from . import strategies


@given(strategies.empty_sets)
def test_base_case(set_: BaseSet) -> None:
    with pytest.raises(ValueError):
        set_.max()


@given(strategies.non_empty_sets)
def test_step(set_: BaseSet) -> None:
    result = set_.max()

    assert result in set_
    assert all(not set_value_to_key(set_, result)
                   < set_value_to_key(set_, value)
               for value in set_)
