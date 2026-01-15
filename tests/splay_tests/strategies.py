from hypothesis import strategies

from dendroid import splay
from dendroid.hints import Order
from tests.hints import KeyT, ValueT
from tests.strategies import (
    non_empty_value_sequence_with_order_strategy,
    to_non_empty_set_with_their_value_strategy,
    two_or_more_values_with_order_strategy,
    value_sequence_with_order_strategy,
)
from tests.utils import BaseSet, ValueSequenceWithOrder


def to_set(
    values_list_with_order: tuple[list[ValueT], Order[ValueT, KeyT] | None], /
) -> BaseSet[ValueT]:
    values_list, order = values_list_with_order
    return splay.set_(*values_list, key=order)


sets = strategies.builds(to_set, value_sequence_with_order_strategy)
non_empty_sets = strategies.builds(
    to_set, non_empty_value_sequence_with_order_strategy
)
non_empty_sets_with_their_values = non_empty_sets.flatmap(
    to_non_empty_set_with_their_value_strategy
)


def is_value_non_max(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> bool:
    set_, value = set_with_value
    return value != set_.max()


non_empty_sets_with_their_non_max_values = (
    non_empty_sets_with_their_values.filter(is_value_non_max)
)


def is_value_non_min(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> bool:
    tree, value = set_with_value
    return value != tree.min()


non_empty_sets_with_their_non_min_values = (
    non_empty_sets_with_their_values.filter(is_value_non_min)
)


def to_set_with_value(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> tuple[BaseSet[ValueT], ValueT]:
    values_list, order = values_list_with_order
    *rest_values_list, value = values_list
    set_ = splay.set_(*rest_values_list, key=order)
    return set_, value


sets_with_values = strategies.builds(
    to_set_with_value, non_empty_value_sequence_with_order_strategy
)
non_empty_sets_with_values = strategies.builds(
    to_set_with_value, two_or_more_values_with_order_strategy
)
