from hypothesis import given

from dendroid.utils import to_balanced_tree_height
from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.trees)
def test_basic(tree: Tree) -> None:
    result = tree.clear()

    assert result is None


@given(strategies.trees)
def test_properties(tree: Tree) -> None:
    tree.clear()

    assert len(tree) == 0
    assert not tree
    assert to_height(tree) == to_balanced_tree_height(len(tree)) == -1
    assert is_left_subtree_less_than_right_subtree(tree)
