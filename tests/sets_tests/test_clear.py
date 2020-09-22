from hypothesis import given

from dendroid.utils import to_balanced_tree_height
from tests.utils import (Set,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.sets)
def test_basic(set_: Set) -> None:
    result = set_.clear()

    assert result is None


@given(strategies.sets)
def test_properties(set_: Set) -> None:
    set_.clear()

    tree = set_.tree
    assert len(set_) == 0
    assert not set_
    assert to_height(tree) == to_balanced_tree_height(len(tree)) == -1
    assert is_left_subtree_less_than_right_subtree(tree)
