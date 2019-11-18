from typing import Tuple

from hypothesis import given

from dendroid import red_black
from dendroid.utils import to_balanced_tree_height
from tests.utils import (are_nodes_parents_to_children,
                         do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black,
                         to_height)
from . import strategies


@given(strategies.trees_pairs)
def test_properties(trees_pair: Tuple[red_black.Tree, red_black.Tree]) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree ^ right_tree

    assert to_height(result) <= 2 * to_balanced_tree_height(len(result) + 1)
    assert are_nodes_parents_to_children(result)
    assert is_root_black(result)
    assert do_red_nodes_have_black_children(result)
    assert do_paths_to_leaves_have_same_black_nodes_count(result)
