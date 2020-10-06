from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import (Item,
                            Key)
from tests.utils import (Map,
                         map_value_to_key)
from . import strategies


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.next(key)


@given(strategies.non_empty_maps_with_their_items)
def test_step(map_with_value: Tuple[Map, Item]) -> None:
    map_, (key, value) = map_with_value

    assert value == map_.max() or key < map_value_to_key(map_, map_.next(key))


@given(strategies.non_empty_maps_with_external_keys)
def test_external_value(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.next(key)


@given(strategies.non_empty_maps)
def test_maximum_key(map_: Map) -> None:
    maximum_key = max(map_)

    with pytest.raises(KeyError):
        map_.next(maximum_key)
