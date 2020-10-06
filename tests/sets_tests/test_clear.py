from hypothesis import given

from tests.utils import (BaseSet,
                         is_left_subtree_less_than_right_subtree,
                         to_balanced_tree_height,
                         to_height)
from . import strategies


@given(strategies.sets)
def test_type(set_: BaseSet) -> None:
    result = set_.clear()

    assert result is None


@given(strategies.sets)
def test_properties(set_: BaseSet) -> None:
    set_.clear()

    tree = set_.tree
    assert len(set_) == 0
    assert to_height(tree) == to_balanced_tree_height(len(tree)) == -1
    assert is_left_subtree_less_than_right_subtree(tree)
