import pytest
from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map, map_value_to_key

from . import strategies


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.flooritem(key)


@given(strategies.non_empty_maps_with_keys)
def test_step(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    try:
        floor_key, _floor = map_.flooritem(key)
    except KeyError:
        assert key < map_value_to_key(map_, map_.min())
    else:
        assert not key < floor_key
        assert all(
            key < map_key or not floor_key < map_key for map_key in map_
        )


@given(strategies.non_empty_maps)
def test_keys(map_: Map[KeyT, ValueT]) -> None:
    assert all(
        map_.flooritem(key) == (key, value) for key, value in map_.items()
    )
