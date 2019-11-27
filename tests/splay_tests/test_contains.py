from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import (Tree,
                         implication,
                         to_height,
                         to_max_binary_tree_height)
from . import strategies


@given(strategies.non_empty_trees_with_values)
def test_properties(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    assert implication(value in tree, tree.root.key == tree._to_key(value))


@given(strategies.non_empty_trees)
def test_accessing_in_order(tree: Tree) -> None:
    for element in tree:
        element in tree

    assert to_height(tree) == to_max_binary_tree_height(tree)
