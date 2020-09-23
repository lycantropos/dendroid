from copy import copy
from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import (Item,
                            Key)
from tests.utils import (Map,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.non_empty_maps_with_their_keys)
def test_properties(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    map_.pop(key)

    tree = map_.tree
    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        map_.pop(key)


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key
    original = copy(map_)

    result = map_.pop(key)

    assert key not in map_
    assert result not in map_.values()
    assert result in original.values()
    assert len(map_) == len(original) - 1


@given(strategies.empty_maps_with_items)
def test_base_case_with_default(map_with_key: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_key

    result = map_.pop(key, default)

    assert result is default


@given(strategies.non_empty_maps_with_items)
def test_step_with_default(map_with_key: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_key
    original = copy(map_)

    result = map_.pop(key, default)

    assert key not in map_
    assert result not in map_.values()
    assert (result in original.values()
            if key in original
            else result is default)
    assert len(map_) == len(original) - (key in original)
