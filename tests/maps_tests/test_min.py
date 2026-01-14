import pytest
from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map

from . import strategies


@given(strategies.empty_maps)
def test_base_case(map_: Map[KeyT, ValueT]) -> None:
    with pytest.raises(KeyError):
        map_.min()


@given(strategies.non_empty_maps)
def test_step(map_: Map[KeyT, ValueT]) -> None:
    result = map_.min()

    assert result in map_.values()
    assert result == min(map_.items())[1]
