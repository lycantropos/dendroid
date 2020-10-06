from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (BaseSet,
                         are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.sets_with_values)
def test_properties(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    set_.discard(value)

    tree = set_.tree
    assert are_nodes_parents_to_children(tree)
    assert are_nodes_heights_correct(tree)
    assert are_balance_factors_normalized(tree)
