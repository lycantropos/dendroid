from hypothesis import given

from tests.utils import (Map,
                         capacity,
                         pairwise)
from . import strategies


@given(strategies.maps)
def test_size(map_: Map) -> None:
    result = reversed(map_)

    assert capacity(result) == len(map_)


@given(strategies.maps)
def test_elements(map_: Map) -> None:
    result = reversed(map_)

    assert all(element in map_ for element in result)


@given(strategies.maps_with_two_or_more_items)
def test_order(map_: Map) -> None:
    result = reversed(map_)

    assert all(next_key < key for key, next_key in pairwise(result))
