from typing import Tuple

from hypothesis import given

from dendroid import red_black
from tests.utils import (are_nodes_parents_to_children,
                         do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black,
                         to_height,
                         to_max_red_black_tree_height)
from . import strategies


@given(strategies.trees_pairs)
def test_properties(trees_pair: Tuple[red_black.Tree, red_black.Tree]) -> None:
    left_tree, right_tree = trees_pair

    left_tree -= right_tree

    assert to_height(left_tree) <= to_max_red_black_tree_height(left_tree)
    assert are_nodes_parents_to_children(left_tree)
    assert is_root_black(left_tree)
    assert do_red_nodes_have_black_children(left_tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(left_tree)
