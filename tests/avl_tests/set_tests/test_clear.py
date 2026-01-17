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


@given(strategies.set_strategy)
def test_properties(set_: BaseSet[ValueT]) -> None:
    set_.clear()

    tree = set_._tree
    assert isinstance(tree, avl.Tree)
    assert are_nodes_parents_to_children(tree)
    assert are_nodes_heights_correct(tree)
    assert are_balance_factors_normalized(tree)
