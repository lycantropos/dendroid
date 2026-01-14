import pytest
from hypothesis import given

from dendroid.hints import Item
from tests.hints import KeyT, ValueT
from tests.utils import Map

from . import strategies


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.previtem(key)


@given(strategies.non_empty_maps_with_their_items)
def test_step(
    map_with_value: tuple[Map[KeyT, ValueT], Item[KeyT, ValueT]],
) -> None:
    map_, (key, value) = map_with_value

    assert value == map_.min() or map_.previtem(key)[0] < key


@given(strategies.non_empty_maps_with_external_keys)
def test_external_value(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.previtem(key)


@given(strategies.non_empty_maps)
def test_minimum_key(map_: Map[KeyT, ValueT]) -> None:
    minimum_key = min(map_)

    with pytest.raises(KeyError):
        map_.previtem(minimum_key)
