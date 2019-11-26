from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import Tree
from . import strategies


@given(strategies.non_empty_trees_with_their_non_max_values)
def test_properties(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    result = tree.next(value)

    assert tree._to_key(result) == tree.root.key
