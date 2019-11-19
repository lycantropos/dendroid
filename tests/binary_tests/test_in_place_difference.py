from typing import Tuple

from hypothesis import given

from dendroid import binary
from tests.utils import (to_height,
                         to_max_binary_tree_height)
from . import strategies


@given(strategies.trees_pairs)
def test_properties(trees_pair: Tuple[binary.Tree, binary.Tree]) -> None:
    left_tree, right_tree = trees_pair

    left_tree -= right_tree

    assert to_height(left_tree) <= to_max_binary_tree_height(left_tree)
