from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import Key
from tests.utils import (Map,
                         map_value_to_key)
from . import strategies


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.floor(key)


@given(strategies.non_empty_maps_with_keys)
def test_step(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    try:
        floor = map_.floor(key)
    except KeyError:
        assert key < map_value_to_key(map_, map_.min())
    else:
        floor_key = map_value_to_key(map_, floor)
        assert (not key < floor_key
                and all(key < map_key or not floor_key < map_key
                        for map_key in map_))


@given(strategies.non_empty_maps)
def test_keys(map_: Map) -> None:
    assert all(map_.floor(key) is value for key, value in map_.items())
