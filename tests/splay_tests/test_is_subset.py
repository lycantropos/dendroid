from hypothesis import given

from dendroid import splay
from tests.utils import (to_height,
                         to_max_binary_tree_height)
from . import strategies


@given(strategies.trees)
def test_properties(tree: splay.Tree) -> None:
    tree <= tree

    assert to_height(tree) == to_max_binary_tree_height(tree)
