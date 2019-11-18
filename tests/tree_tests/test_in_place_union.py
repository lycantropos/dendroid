from copy import deepcopy

from hypothesis import given

from dendroid.utils import to_balanced_tree_height
from tests.utils import (TreesPair,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.trees_pairs)
def test_connection_with_intersection(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair
    original_left_tree = deepcopy(left_tree)

    left_tree |= right_tree

    assert left_tree == original_left_tree | right_tree


@given(strategies.trees_pairs)
def test_properties(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    left_tree |= right_tree

    assert len(left_tree) >= len(right_tree)
    assert to_height(left_tree) >= to_balanced_tree_height(len(left_tree))
    assert all(value in left_tree
               for value in right_tree)
    assert not right_tree or not left_tree.isdisjoint(right_tree)
    assert is_left_subtree_less_than_right_subtree(left_tree)
