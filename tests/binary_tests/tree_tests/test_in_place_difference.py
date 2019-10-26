from copy import deepcopy
from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from . import strategies


@given(strategies.trees_pairs)
def test_connection_with_intersection(trees_pair: Tuple[Tree, Tree]) -> None:
    left_tree, right_tree = trees_pair
    original_left_tree = deepcopy(left_tree)

    left_tree -= right_tree

    assert left_tree == original_left_tree - right_tree
