from copy import deepcopy

from hypothesis import given

from tests.utils import TreesPair
from . import strategies


@given(strategies.trees_pairs)
def test_connection_with_intersection(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair
    original_left_tree = deepcopy(left_tree)

    left_tree ^= right_tree

    assert left_tree == original_left_tree ^ right_tree
