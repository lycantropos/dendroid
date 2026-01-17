from hypothesis import given

from dendroid import avl
from tests import strategies
from tests.hints import KeyT, ValueT
from tests.utils import (
    BaseSet,
    ValueSequenceWithOrder,
    are_balance_factors_normalized,
    are_nodes_heights_correct,
    are_nodes_parents_to_children,
    is_left_subtree_less_than_right_subtree,
    to_balanced_tree_height,
    to_height,
)


@given(strategies.value_sequence_with_order_strategy)
def test_type(values_with_order: ValueSequenceWithOrder[ValueT, KeyT]) -> None:
    values, order = values_with_order

    result = avl.set_(*values, key=order)

    assert isinstance(result, BaseSet)


@given(strategies.value_sequence_with_order_strategy)
def test_properties(
    values_with_order: ValueSequenceWithOrder[ValueT, KeyT],
) -> None:
    values, order = values_with_order

    result = avl.set_(*values, key=order)

    result_tree = result._tree
    assert isinstance(result_tree, avl.Tree)
    assert len(result) <= len(values)
    assert to_height(result_tree) == to_balanced_tree_height(len(result))
    assert all(value in result for value in values)
    assert all(value in values for value in result)
    assert is_left_subtree_less_than_right_subtree(result_tree)
    assert are_nodes_parents_to_children(result_tree)
    assert are_nodes_heights_correct(result_tree)
    assert are_balance_factors_normalized(result_tree)


@given(strategies.value_sequence_with_order_strategy)
def test_base_case(
    values_with_order: ValueSequenceWithOrder[ValueT, KeyT],
) -> None:
    values, order = values_with_order

    result: BaseSet[ValueT] = avl.set_(key=order)

    assert len(result) == 0
    assert not result
    assert all(value not in result for value in values)


@given(strategies.non_empty_value_sequence_with_order_strategy)
def test_step(values_with_order: ValueSequenceWithOrder[ValueT, KeyT]) -> None:
    values, order = values_with_order
    *values, value = values

    result = avl.set_(*values, key=order)
    next_result = avl.set_(*values, value, key=order)

    assert next_result
    assert len(next_result) == (
        len(result)
        + (
            value not in values
            if order is None
            else order(value) not in map(order, values)
        )
    )
    assert value in next_result
    assert all(value in next_result for value in result)
