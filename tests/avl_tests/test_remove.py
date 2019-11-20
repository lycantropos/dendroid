from typing import Tuple

from hypothesis import given

from dendroid import avl
from dendroid.hints import Domain
from tests.utils import (are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.non_empty_trees_with_their_values)
def test_properties(tree_with_value: Tuple[avl.Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.remove(value)

    assert are_nodes_parents_to_children(tree)
    assert are_nodes_heights_correct(tree)
    assert are_balance_factors_normalized(tree)
