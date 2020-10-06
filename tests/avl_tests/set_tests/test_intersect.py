from typing import Tuple

from hypothesis import given

from tests.utils import (BaseSet,
                         are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.sets_pairs)
def test_properties(sets_pair: Tuple[BaseSet, BaseSet]) -> None:
    left_set, right_set = sets_pair

    result = left_set & right_set

    result_tree = result.tree
    assert are_nodes_parents_to_children(result_tree)
    assert are_nodes_heights_correct(result_tree)
    assert are_balance_factors_normalized(result_tree)
