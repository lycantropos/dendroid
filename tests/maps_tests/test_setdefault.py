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


@given(strategies.non_empty_maps_with_their_keys)
def test_properties(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    map_.setdefault(key)

    tree = map_.tree
    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key

    result = map_.setdefault(key)

    assert result is map_[key] is None


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: Tuple[Map, Key]) -> None:
    map_, key = map_with_key
    original = copy(map_)

    result = map_.setdefault(key)

    assert key in map_
    assert result in map_.values()
    assert result == original[key] if key in original else result is None
    assert len(map_) == len(original) + (key not in original)


@given(strategies.empty_maps_with_items)
def test_base_case_with_default(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_item

    result = map_.setdefault(key, default)

    assert result is map_[key] is default


@given(strategies.non_empty_maps_with_items)
def test_step_with_default(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, default) = map_with_item
    original = copy(map_)

    result = map_.setdefault(key, default)

    assert key in map_
    assert result in map_.values()
    assert (result is original[key]
            if key in original
            else result is default)
    assert len(map_) == len(original) + (key not in original)
