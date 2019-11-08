from typing import Tuple

from hypothesis import given

from dendroid import red_black
from tests.utils import (do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black)
from . import strategies


@given(strategies.trees_pairs)
def test_properties(trees_pair: Tuple[red_black.Tree, red_black.Tree]) -> None:
    left_tree, right_tree = trees_pair

    left_tree |= right_tree

    assert is_root_black(left_tree)
    assert do_red_nodes_have_black_children(left_tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(left_tree)