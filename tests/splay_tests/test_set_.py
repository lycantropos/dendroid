from hypothesis import given

from dendroid import splay
from tests import strategies
from tests.utils import (Set,
                         ValuesListWithOrder,
                         is_left_subtree_less_than_right_subtree,
                         to_balanced_tree_height,
                         to_height)


@given(strategies.values_lists_with_orders)
def test_basic(values_with_order: ValuesListWithOrder) -> None:
    values, order = values_with_order

    result = splay.set_(*values,
                        key=order)

    assert isinstance(result, Set)


@given(strategies.values_lists_with_orders)
def test_properties(values_with_order: ValuesListWithOrder) -> None:
    values, order = values_with_order

    result = splay.set_(*values,
                        key=order)

    result_tree = result.tree
    assert len(result) <= len(values)
    assert to_height(result_tree) == to_balanced_tree_height(len(result_tree))
    assert all(value in result for value in values)
    assert all(value in values for value in result)
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.values_lists_with_orders)
def test_base_case(values_with_order: ValuesListWithOrder) -> None:
    values, order = values_with_order

    result = splay.set_(key=order)

    assert len(result) == 0
    assert not result
    assert all(value not in result for value in values)


@given(strategies.non_empty_values_lists_with_orders)
def test_step(values_with_order: ValuesListWithOrder) -> None:
    values, order = values_with_order
    *values, value = values

    result = splay.set_(*values,
                        key=order)
    next_result = splay.set_(*values, value,
                             key=order)

    assert next_result
    assert len(next_result) == (len(result)
                                + (value not in values
                                   if order is None
                                   else order(value) not in map(order,
                                                                values)))
    assert value in next_result
    assert all(value in next_result for value in result)
