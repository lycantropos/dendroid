from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.non_empty_sets_with_their_values)
def test_properties(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    set_.remove(value)

    tree = set_.tree
    assert are_nodes_parents_to_children(tree)
    assert are_nodes_heights_correct(tree)
    assert are_balance_factors_normalized(tree)
