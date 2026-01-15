from hypothesis import given

from dendroid import avl
from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    are_balance_factors_normalized,
    are_nodes_heights_correct,
    are_nodes_parents_to_children,
)

from . import strategies


@given(strategies.set_pair_strategy)
def test_properties(
    sets_pair: tuple[BaseSet[ValueT], BaseSet[ValueT]],
) -> None:
    left_set, right_set = sets_pair

    left_set &= right_set

    left_tree = left_set.tree
    assert isinstance(left_tree, avl.Tree)
    assert are_nodes_parents_to_children(left_tree)
    assert are_nodes_heights_correct(left_tree)
    assert are_balance_factors_normalized(left_tree)
