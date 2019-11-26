from typing import Tuple

from hypothesis import given

from dendroid import splay
from dendroid.hints import Domain
from . import strategies


@given(strategies.trees_with_values)
def test_properties(tree_with_value: Tuple[splay.Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.add(value)

    assert tree.root.key == tree._to_key(value)
