from hypothesis import given

from tests.utils import (Map,
                         is_left_subtree_less_than_right_subtree,
                         to_balanced_tree_height,
                         to_height)
from . import strategies


@given(strategies.maps)
def test_type(map_: Map) -> None:
    result = map_.clear()

    assert result is None


@given(strategies.maps)
def test_properties(map_: Map) -> None:
    map_.clear()

    tree = map_.tree
    assert len(map_) == 0
    assert to_height(tree) == to_balanced_tree_height(len(tree)) == -1
    assert is_left_subtree_less_than_right_subtree(tree)
