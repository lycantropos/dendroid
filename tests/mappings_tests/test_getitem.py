from copy import copy
from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import Key
from tests.utils import (Map,
                         are_keys_equal,
                         one)
from . import strategies


@given(strategies.non_empty_maps_with_their_keys)
def test_immutability(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key
    original = copy(map_)

    map_[key]

    assert map_ == original


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_item: Tuple[Map, Key]) -> None:
    map_, key = map_with_item

    with pytest.raises(KeyError):
        map_[key]


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    value = map_[key]

    assert one(are_keys_equal(key, node.key) and node.value is value
               for node in map_.tree)
