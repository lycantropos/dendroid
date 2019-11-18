from hypothesis import given

from dendroid import red_black
from dendroid.utils import to_balanced_tree_height
from tests.utils import (are_nodes_parents_to_children,
                         do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black,
                         to_height)
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: red_black.Tree) -> None:
    tree.popmin()

    assert to_height(tree) <= 2 * to_balanced_tree_height(len(tree) + 1)
    assert are_nodes_parents_to_children(tree)
    assert is_root_black(tree)
    assert do_red_nodes_have_black_children(tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(tree)
