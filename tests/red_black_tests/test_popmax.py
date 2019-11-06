from hypothesis import given

from dendroid import red_black
from tests.utils import (do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black)
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: red_black.Tree) -> None:
    tree.popmax()

    assert is_root_black(tree)
    assert do_red_nodes_have_black_children(tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(tree)
