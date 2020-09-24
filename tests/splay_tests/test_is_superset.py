from hypothesis import given

from tests.utils import (Set,
                         to_height,
                         to_max_binary_tree_height)
from . import strategies


@given(strategies.sets)
def test_properties(set_: Set) -> None:
    set_ >= set_

    tree = set_.tree
    assert to_height(tree) == to_max_binary_tree_height(tree)
