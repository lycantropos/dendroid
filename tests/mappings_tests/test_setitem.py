from copy import copy
from typing import Tuple

from hypothesis import given

from dendroid.hints import Item
from tests.utils import (Map,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.maps_with_items)
def test_properties(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, value) = map_with_item

    map_[key] = value

    tree = map_.tree
    assert len(map_) > 0
    assert (max(0, to_min_binary_tree_height(tree))
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_maps_with_items)
def test_base_case(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, value) = map_with_item

    map_[key] = value

    assert len(map_) == 1
    assert key in map_
    assert map_[key] is value


@given(strategies.non_empty_maps_with_items)
def test_step(map_with_item: Tuple[Map, Item]) -> None:
    map_, (key, value) = map_with_item
    original = copy(map_)

    map_[key] = value

    assert len(map_) == len(original) + (key not in original)
    assert key in map_
    assert map_[key] is value
