from typing import Tuple

from hypothesis import given

from dendroid import splay
from dendroid.hints import Domain
from . import strategies


@given(strategies.non_empty_trees_with_their_non_min_values)
def test_properties(tree_with_value: Tuple[splay.Tree, Domain]) -> None:
    tree, value = tree_with_value

    result = tree.prev(value)

    assert tree._to_key(result) == tree.root.key
