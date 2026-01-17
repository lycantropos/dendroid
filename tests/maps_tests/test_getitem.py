from copy import copy

import pytest
from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import (
    Map,
    are_keys_equal,
    is_left_subtree_less_than_right_subtree,
    one,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.non_empty_maps_with_their_keys)
def test_properties(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    map_[key]

    tree = map_._tree
    assert (
        to_min_binary_tree_height(tree)
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.non_empty_maps_with_their_keys)
def test_immutability(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key
    original = copy(map_)

    map_[key]

    assert map_ == original


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_item: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_item

    with pytest.raises(KeyError):
        map_[key]


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    value = map_[key]

    assert one(
        are_keys_equal(key, node.key) and node.value is value
        for node in map_._tree
    )
