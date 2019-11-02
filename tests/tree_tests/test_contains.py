from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from dendroid.hints import Domain
from . import strategies


@given(strategies.trees_with_totally_ordered_values)
def test_basic(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    result = value in tree

    assert isinstance(result, bool)