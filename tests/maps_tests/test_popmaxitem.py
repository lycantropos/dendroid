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


@given(strategies.non_empty_maps)
def test_properties(map_: Map[KeyT, ValueT]) -> None:
    map_.popmaxitem()

    tree = map_._tree
    assert (
        to_min_binary_tree_height(tree)
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_maps)
def test_base_case(map_: Map[KeyT, ValueT]) -> None:
    with pytest.raises(KeyError):
        map_.popmaxitem()


@given(strategies.non_empty_maps)
def test_step(map_: Map[KeyT, ValueT]) -> None:
    original = copy(map_)

    result = map_.popmaxitem()

    assert result not in map_.items()
    assert result in original.items()
    assert result == original.maxitem()
    assert len(map_) == len(original) - 1
