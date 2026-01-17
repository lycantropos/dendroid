from copy import copy

import pytest
from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import (
    Map,
    is_left_subtree_less_than_right_subtree,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.non_empty_maps_with_their_keys)
def test_properties(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    del map_[key]

    tree = map_._tree
    assert (
        to_min_binary_tree_height(tree)
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_maps_with_keys)
def test_base_case(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key

    with pytest.raises(KeyError):
        del map_[key]


@given(strategies.non_empty_maps_with_their_keys)
def test_step(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> None:
    map_, key = map_with_key
    original = copy(map_)

    del map_[key]

    assert map_ != original
    assert len(map_) == len(original) - 1
    assert key not in map_
    assert map_.keys() < original.keys()
    assert all(original[key] == value for key, value in map_.items())
