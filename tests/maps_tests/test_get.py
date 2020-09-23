from copy import copy
from typing import Tuple

from hypothesis import given

from dendroid.hints import (Item,
                            Key)
from tests.utils import (Map,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.non_empty_maps_with_items)
def test_properties(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_item

    map_.get(key, default)

    tree = map_.tree
    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.non_empty_maps_with_items)
def test_immutability(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_item
    original = copy(map_)

    map_.get(key, default)

    assert map_ == original


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    assert map_.get(key) is None


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    result = map_.get(key)

    assert result == map_[key] if key in map_ else result is None


@given(strategies.empty_maps_with_items)
def test_base_case_with_default(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_item

    result = map_.get(key, default)

    assert result is default


@given(strategies.non_empty_maps_with_items)
def test_step_with_default(map_with_key: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_key
    map_ = copy(map_)

    result = map_.get(key, default)

    assert result == map_[key] if key in map_ else result is default
