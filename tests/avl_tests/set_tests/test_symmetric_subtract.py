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

    result = left_set ^ right_set

    result_tree = result._tree
    assert isinstance(result_tree, avl.Tree)
    assert are_nodes_parents_to_children(result_tree)
    assert are_nodes_heights_correct(result_tree)
    assert are_balance_factors_normalized(result_tree)
