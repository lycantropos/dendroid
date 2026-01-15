from functools import partial

from hypothesis import strategies as st

from dendroid import red_black
from tests.hints import KeyT, ValueT
from tests.strategies import (
    non_empty_value_sequence_with_order_strategy,
    to_value_sequences_with_order_strategy,
    value_sequence_with_order_strategy,
    value_with_order_strategy_strategy,
)
from tests.utils import (
    BaseSet,
    ValueSequencePairWithOrder,
    ValueSequenceWithOrder,
)


def to_set(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> BaseSet[ValueT]:
    values_list, key = values_list_with_order
    return red_black.set_(*values_list, key=key)


sets = st.builds(to_set, value_sequence_with_order_strategy)
non_empty_sets = st.builds(
    to_set, non_empty_value_sequence_with_order_strategy
)


def to_set_with_value(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> tuple[BaseSet[ValueT], ValueT]:
    values_list, order = values_list_with_order
    *rest_values_list, value = values_list
    set_ = red_black.set_(*rest_values_list, key=order)
    return set_, value


sets_with_values = st.builds(
    to_set_with_value, non_empty_value_sequence_with_order_strategy
)


def to_non_empty_sets_with_their_values(
    set_: BaseSet[ValueT], /
) -> st.SearchStrategy[tuple[BaseSet[ValueT], ValueT]]:
    return st.tuples(st.just(set_), st.sampled_from(list(set_)))


non_empty_sets_with_their_values = non_empty_sets.flatmap(
    to_non_empty_sets_with_their_values
)


def to_sets_pair(
    value_sequences_pair_with_order: ValueSequencePairWithOrder[ValueT, KeyT],
    /,
) -> tuple[BaseSet[ValueT], BaseSet[ValueT]]:
    (first_values_list, second_values_list), order = (
        value_sequences_pair_with_order
    )
    return (
        red_black.set_(*first_values_list, key=order),
        red_black.set_(*second_values_list, key=order),
    )


sets_pairs = st.builds(
    to_sets_pair,
    value_with_order_strategy_strategy.flatmap(
        partial(to_value_sequences_with_order_strategy, sizes=[(0, None)] * 2)
    ),
)
