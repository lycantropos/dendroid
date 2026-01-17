from hypothesis import given

from dendroid import red_black
from tests import strategies
from tests.hints import KeyT, ValueT
from tests.utils import (
    BaseSet,
    ValueSequenceWithOrder,
    are_nodes_parents_to_children,
    do_paths_to_leaves_have_same_black_nodes_count,
    do_red_nodes_have_black_children,
    is_left_subtree_less_than_right_subtree,
    is_root_black,
    to_balanced_tree_height,
    to_height,
)


@given(strategies.value_sequence_with_order_strategy)
def test_type(values_with_order: ValueSequenceWithOrder[ValueT, KeyT]) -> None:
    values, key = values_with_order

    result = red_black.set_(*values, key=key)

    assert isinstance(result, BaseSet)


@given(strategies.value_sequence_with_order_strategy)
def test_properties(
    values_with_order: ValueSequenceWithOrder[ValueT, KeyT],
) -> None:
    values, key = values_with_order

    result = red_black.set_(*values, key=key)

    result_tree = result._tree
    assert isinstance(result_tree, red_black.Tree)
    assert len(result) <= len(values)
    assert to_height(result_tree) == to_balanced_tree_height(len(result))
    assert all(value in result for value in values)
    assert all(value in values for value in result)
    assert is_left_subtree_less_than_right_subtree(result_tree)
    assert are_nodes_parents_to_children(result_tree)
    assert is_root_black(result_tree)
    assert do_red_nodes_have_black_children(result_tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(result_tree)


@given(strategies.value_sequence_with_order_strategy)
def test_base_case(
    values_with_order: ValueSequenceWithOrder[ValueT, KeyT],
) -> None:
    values, key = values_with_order

    result: BaseSet[ValueT] = red_black.set_(key=key)

    assert len(result) == 0
    assert not result
    assert all(value not in result for value in values)


@given(strategies.non_empty_value_sequence_with_order_strategy)
def test_step(values_with_order: ValueSequenceWithOrder[ValueT, KeyT]) -> None:
    values, key = values_with_order
    *values, value = values

    result = red_black.set_(*values, key=key)
    next_result = red_black.set_(*values, value, key=key)

    assert next_result
    assert len(next_result) == (
        len(result)
        + (
            value not in values
            if key is None
            else key(value) not in map(key, values)
        )
    )
    assert value in next_result
    assert all(value in next_result for value in result)
