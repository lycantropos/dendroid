import math
from functools import partial
from operator import not_
from typing import Any

from hypothesis import strategies as st

from dendroid.hints import Order
from tests.hints import KeyT, ValueT
from tests.utils import (
    ValueSequenceWithOrder,
    combine,
    compose,
    identity,
    leap_traverse,
    to_constant,
)

from .factories import (
    to_value_sequence_with_order_strategy,
    to_value_with_order_strategy,
    to_values_tuples_with_orders,
)

maybe_infinite_numbers_orders = st.sampled_from([identity, abs])
finite_numbers_orders = maybe_infinite_numbers_orders | st.sampled_from(
    [round, math.trunc, math.ceil, math.floor]
)
strings_orders = st.sampled_from(
    [
        identity,
        str.lower,
        str.upper,
        str.title,
        str.capitalize,
        str.casefold,
        str.swapcase,
    ]
)
base_values_with_orders_strategies: st.SearchStrategy[
    tuple[st.SearchStrategy[Any], st.SearchStrategy[Order[Any, Any]]]
] = st.sampled_from(
    [
        (st.integers(), finite_numbers_orders),
        (st.floats(allow_nan=False), maybe_infinite_numbers_orders),
        (
            st.floats(allow_nan=False, allow_infinity=False),
            finite_numbers_orders,
        ),
        (st.booleans(), st.just(not_) | finite_numbers_orders),
        (st.text(), strings_orders),
    ]
)
value_with_order_strategy_strategy = st.recursive(
    base_values_with_orders_strategies,
    to_values_tuples_with_orders,
    max_leaves=10,
)
value_with_order_strategy = value_with_order_strategy_strategy.flatmap(
    to_value_with_order_strategy
)


def to_different_values_orders(
    lists_with_orders: st.SearchStrategy[ValueSequenceWithOrder[ValueT, KeyT]],
    /,
) -> st.SearchStrategy[ValueSequenceWithOrder[ValueT, KeyT]]:
    return (
        lists_with_orders
        | (
            lists_with_orders.map(
                compose(
                    tuple, combine(partial(sorted, reverse=True), identity)
                )
            )
        )
        | lists_with_orders.map(compose(tuple, combine(sorted, identity)))
        | (
            lists_with_orders.map(
                compose(tuple, combine(leap_traverse, identity))
            )
        )
    )


value_sequence_with_order_strategy = to_different_values_orders(
    value_with_order_strategy_strategy.flatmap(
        partial(to_value_sequence_with_order_strategy, min_size=0)
    )
)
value_sequence_with_none_order_strategy = (
    value_sequence_with_order_strategy.map(
        compose(tuple, combine(identity, to_constant(None)))
    )
)
empty_value_sequence_with_order_strategy = (
    value_with_order_strategy_strategy.flatmap(
        partial(to_value_sequence_with_order_strategy, min_size=0, max_size=0)
    )
)
non_empty_value_sequence_with_order_strategy = to_different_values_orders(
    value_with_order_strategy_strategy.flatmap(
        partial(to_value_sequence_with_order_strategy, min_size=1)
    )
)
single_value_with_order_strategy = value_with_order_strategy_strategy.flatmap(
    partial(to_value_sequence_with_order_strategy, min_size=1, max_size=1)
)
two_or_more_values_with_order_strategy = to_different_values_orders(
    value_with_order_strategy_strategy.flatmap(
        partial(to_value_sequence_with_order_strategy, min_size=2)
    )
)
