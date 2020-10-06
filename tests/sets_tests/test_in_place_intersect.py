from copy import copy

from hypothesis import given

from tests.utils import (BaseSetsPair,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.sets_pairs)
def test_connection_with_intersection(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair
    original_left_set = copy(left_set)

    left_set &= right_set

    assert left_set == original_left_set & right_set


@given(strategies.sets_pairs)
def test_properties(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair

    left_set &= right_set

    left_tree = left_set.tree
    assert len(left_set) <= len(right_set)
    assert (to_min_binary_tree_height(left_tree)
            <= to_height(left_tree)
            <= to_max_binary_tree_height(left_tree))
    assert all(value in right_set
               for value in left_set)
    assert not left_set or not left_set.isdisjoint(right_set)
    assert is_left_subtree_less_than_right_subtree(left_tree)
