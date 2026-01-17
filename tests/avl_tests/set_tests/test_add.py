from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    AvlTree,
    BaseSet,
    are_balance_factors_normalized,
    are_nodes_heights_correct,
    are_nodes_parents_to_children,
)

from . import strategies


@given(strategies.set_with_value_strategy)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    set_.add(value)

    tree = set_._tree
    assert isinstance(tree, AvlTree)
    assert are_nodes_parents_to_children(tree)
    assert are_nodes_heights_correct(tree)
    assert are_balance_factors_normalized(tree)
