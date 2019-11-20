from typing import Tuple

from hypothesis import given

from dendroid import avl
from tests.utils import (are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.trees_pairs)
def test_properties(trees_pair: Tuple[avl.Tree, avl.Tree]) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree & right_tree

    assert are_nodes_parents_to_children(result)
    assert are_nodes_heights_correct(result)
    assert are_balance_factors_normalized(result)
