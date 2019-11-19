from typing import Tuple

from hypothesis import given

from dendroid import binary
from dendroid.hints import Domain
from tests.utils import (to_height,
                         to_max_binary_tree_height)
from . import strategies


@given(strategies.trees_with_values)
def test_properties(tree_with_value: Tuple[binary.Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.discard(value)

    assert to_height(tree) <= to_max_binary_tree_height(tree)
