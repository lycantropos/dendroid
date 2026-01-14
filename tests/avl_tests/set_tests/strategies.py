from functools import partial

from hypothesis import strategies as st

from dendroid import avl
from tests.hints import KeyT, ValueT
from tests.strategies import (
    non_empty_values_lists_with_orders,
    to_values_lists_with_orders,
    values_lists_with_orders,
    values_with_orders_strategies,
)
from tests.utils import (
    BaseSet,
    ValueSequencePairWithOrder,
    ValueSequenceWithOrder,
)


def to_set(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> BaseSet[ValueT]:
    values_list, order = values_list_with_order
    return avl.set_(*values_list, key=order)


sets = st.builds(to_set, values_lists_with_orders)
non_empty_sets = st.builds(to_set, non_empty_values_lists_with_orders)


def to_set_with_value(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> tuple[BaseSet[ValueT], ValueT]:
    values_list, order = values_list_with_order
    *rest_values_list, value = values_list
    return (avl.set_(*rest_values_list, key=order), value)


sets_with_values = st.builds(
    to_set_with_value, non_empty_values_lists_with_orders
)


def to_non_empty_sets_with_their_values(
    set_: BaseSet[ValueT], /
) -> st.SearchStrategy[tuple[BaseSet[ValueT], ValueT]]:
    return st.tuples(st.just(set_), st.sampled_from(list(set_)))


non_empty_sets_with_their_values = non_empty_sets.flatmap(
    to_non_empty_sets_with_their_values
)


def to_sets_pair(
    values_lists_pair_with_order: ValueSequencePairWithOrder[ValueT, KeyT], /
) -> tuple[BaseSet[ValueT], BaseSet[ValueT]]:
    (first_values_list, second_values_list), order = (
        values_lists_pair_with_order
    )
    return (
        avl.set_(*first_values_list, key=order),
        avl.set_(*second_values_list, key=order),
    )


sets_pairs = st.builds(
    to_sets_pair,
    values_with_orders_strategies.flatmap(
        partial(to_values_lists_with_orders, sizes=[(0, None)] * 2)
    ),
)
