from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, to_height, to_max_binary_tree_height

from . import strategies


@given(strategies.sets)
def test_properties(set_: BaseSet[ValueT]) -> None:
    _ = set_ <= set_

    tree = set_._tree
    assert to_height(tree) == to_max_binary_tree_height(tree)
