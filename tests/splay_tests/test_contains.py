from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import (Tree,
                         implication)
from . import strategies


@given(strategies.non_empty_trees_with_values)
def test_properties(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    assert implication(value in tree, tree.root.key == tree._to_key(value))
