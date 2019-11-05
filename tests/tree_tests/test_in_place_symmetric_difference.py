from copy import deepcopy

from hypothesis import given

from tests.utils import (TreesPair,
                         is_left_subtree_less_than_right_subtree)
from . import strategies


@given(strategies.trees_pairs)
def test_connection_with_intersection(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair
    original_left_tree = deepcopy(left_tree)

    left_tree ^= right_tree

    assert left_tree == original_left_tree ^ right_tree


@given(strategies.trees_pairs)
def test_properties(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    left_tree ^= right_tree

    assert (not right_tree
            or any(value in left_tree
                   for value in right_tree)
            or not left_tree)
    assert is_left_subtree_less_than_right_subtree(left_tree)
