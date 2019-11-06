from typing import Tuple

from hypothesis import given

from dendroid import red_black
from dendroid.hints import Domain
from tests.utils import (do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black)
from . import strategies


@given(strategies.trees_with_values)
def test_properties(tree_with_value: Tuple[red_black.Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.discard(value)

    assert is_root_black(tree)
    assert do_red_nodes_have_black_children(tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(tree)
