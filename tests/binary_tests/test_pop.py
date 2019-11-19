from hypothesis import given

from dendroid import binary
from tests.utils import (to_height,
                         to_max_binary_tree_height)
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: binary.Tree) -> None:
    tree.pop()

    assert to_height(tree) <= to_max_binary_tree_height(tree)
