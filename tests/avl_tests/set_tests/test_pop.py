from hypothesis import given

from tests.utils import (Set,
                         are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.non_empty_sets)
def test_properties(set_: Set) -> None:
    set_.pop()

    tree = set_.tree
    assert are_nodes_parents_to_children(tree)
    assert are_nodes_heights_correct(tree)
    assert are_balance_factors_normalized(tree)
