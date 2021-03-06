import pytest
from hypothesis import given

from tests.utils import Map
from . import strategies


@given(strategies.empty_maps)
def test_base_case(map_: Map) -> None:
    with pytest.raises(KeyError):
        map_.minitem()


@given(strategies.non_empty_maps)
def test_step(map_: Map) -> None:
    result = map_.minitem()

    assert result in map_.items()
    assert result == min(map_.items())
