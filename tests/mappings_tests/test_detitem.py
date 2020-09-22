from copy import copy
from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import Key
from tests.utils import Map
from . import strategies


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_item: Tuple[Map, Key]) -> None:
    map_, key = map_with_item

    with pytest.raises(KeyError):
        del map_[key]


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key
    original = copy(map_)

    del map_[key]

    assert map_ != original
    assert len(map_) == len(original) - 1
    assert key not in map_
    assert map_.keys() < original.keys()
    assert all(original[key] == value for key, value in map_.items())
