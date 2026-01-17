from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import (
    Map,
    is_left_subtree_less_than_right_subtree,
    to_balanced_tree_height,
    to_height,
)

from . import strategies


@given(strategies.maps)
def test_type(map_: Map[KeyT, ValueT]) -> None:
    result = map_.clear()  # type: ignore[func-returns-value]

    assert result is None


@given(strategies.maps)
def test_properties(map_: Map[KeyT, ValueT]) -> None:
    map_.clear()

    tree = map_._tree
    assert len(map_) == 0
    assert to_height(tree) == to_balanced_tree_height(len(tree)) == -1
    assert is_left_subtree_less_than_right_subtree(tree)
