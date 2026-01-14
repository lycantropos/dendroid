from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map, capacity, pairwise

from . import strategies


@given(strategies.maps)
def test_size(map_: Map[KeyT, ValueT]) -> None:
    result = iter(map_)

    assert capacity(result) == len(map_)


@given(strategies.maps)
def test_elements(map_: Map[KeyT, ValueT]) -> None:
    result = iter(map_)

    assert all(element in map_ for element in result)


@given(strategies.maps_with_two_or_more_items)
def test_order(map_: Map[KeyT, ValueT]) -> None:
    result = iter(map_)

    assert all(key < next_key for key, next_key in pairwise(result))
