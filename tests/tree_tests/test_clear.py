from hypothesis import given

from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree)
from . import strategies


@given(strategies.trees)
def test_basic(tree: Tree) -> None:
    result = tree.clear()

    assert result is None


@given(strategies.trees)
def test_properties(tree: Tree) -> None:
    tree.clear()

    assert len(tree) == 0
    assert is_left_subtree_less_than_right_subtree(tree)
