from hypothesis import given

from dendroid import avl
from dendroid.utils import to_balanced_tree_height
from tests import strategies
from tests.utils import (Set,
                         ValuesListWithKey,
                         are_balance_factors_normalized,
                         are_nodes_heights_correct,
                         are_nodes_parents_to_children,
                         is_left_subtree_less_than_right_subtree,
                         to_height)


@given(strategies.values_lists_with_keys)
def test_basic(values_with_key: ValuesListWithKey) -> None:
    values, key = values_with_key

    result = avl.set_(*values,
                      key=key)

    assert isinstance(result, Set)


@given(strategies.values_lists_with_keys)
def test_properties(values_with_key: ValuesListWithKey) -> None:
    values, key = values_with_key

    result = avl.set_(*values,
                      key=key)

    result_tree = result.tree
    assert len(result) <= len(values)
    assert to_height(result_tree) == to_balanced_tree_height(len(result))
    assert all(value in result for value in values)
    assert all(value in values for value in result)
    assert is_left_subtree_less_than_right_subtree(result_tree)
    assert are_nodes_parents_to_children(result_tree)
    assert are_nodes_heights_correct(result_tree)
    assert are_balance_factors_normalized(result_tree)


@given(strategies.values_lists_with_keys)
def test_base_case(values_with_key: ValuesListWithKey) -> None:
    values, key = values_with_key

    result = avl.set_(key=key)

    assert len(result) == 0
    assert not result
    assert all(value not in result for value in values)


@given(strategies.non_empty_values_lists_with_keys)
def test_step(values_with_key: ValuesListWithKey) -> None:
    values, key = values_with_key
    *values, value = values

    result = avl.set_(*values,
                      key=key)
    next_result = avl.set_(*values, value,
                           key=key)

    assert next_result
    assert len(next_result) == (len(result)
                                + (value not in values
                                   if key is None
                                   else key(value) not in map(key, values)))
    assert value in next_result
    assert all(value in next_result for value in result)
