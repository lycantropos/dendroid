import pytest
from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map

from . import strategies


@given(strategies.empty_maps)
def test_base_case(map_: Map[KeyT, ValueT]) -> None:
    with pytest.raises(KeyError):
        map_.maxitem()


@given(strategies.non_empty_maps)
def test_step(map_: Map[KeyT, ValueT]) -> None:
    result = map_.maxitem()

    assert result in map_.items()
    assert result == max(map_.items())
