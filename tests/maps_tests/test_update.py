from hypothesis import given

from dendroid.hints import Item
from tests.hints import KeyT, ValueT
from tests.utils import Map, MapsPair

from . import strategies


@given(strategies.maps_with_items_lists_or_maps)
def test_type(
    map_with_items_or_map: tuple[
        Map[KeyT, ValueT], list[Item[KeyT, ValueT]] | Map[KeyT, ValueT]
    ],
) -> None:
    map_, items_or_map = map_with_items_or_map

    result = map_.update(items_or_map)  # type: ignore[func-returns-value]

    assert result is None


@given(strategies.maps_pairs)
def test_keys(maps_pair: MapsPair[KeyT, ValueT]) -> None:
    left, right = maps_pair

    left.update(right)

    assert right.keys() <= left.keys()


@given(strategies.maps_pairs)
def test_values(maps_pair: MapsPair[KeyT, ValueT]) -> None:
    left, right = maps_pair

    left.update(right)

    assert all(value in left.values() for value in right.values())


@given(strategies.maps_pairs)
def test_items(maps_pair: MapsPair[KeyT, ValueT]) -> None:
    left, right = maps_pair

    left.update(right)

    assert right.items() <= left.items()
