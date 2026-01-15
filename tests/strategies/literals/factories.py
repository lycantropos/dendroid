from collections.abc import Sequence
from functools import partial

from hypothesis import strategies as st

from dendroid.hints import Order
from tests.hints import KeyT, ValueT
from tests.utils import (
    BaseSet,
    ValueSequenceWithOrder,
    ValueSequencesWithOrder,
)


def to_values_tuples_with_orders(
    values_with_orders: st.SearchStrategy[
        tuple[
            st.SearchStrategy[ValueT], st.SearchStrategy[Order[ValueT, KeyT]]
        ]
    ],
    /,
) -> st.SearchStrategy[
    tuple[
        st.SearchStrategy[Sequence[ValueT]],
        st.SearchStrategy[Order[Sequence[ValueT], tuple[KeyT, ...]]],
    ]
]:
    def to_values_tuples_with_order(
        values_with_orders_list: Sequence[
            tuple[
                st.SearchStrategy[ValueT],
                st.SearchStrategy[Order[ValueT, KeyT]],
            ]
        ],
        /,
    ) -> tuple[
        st.SearchStrategy[Sequence[ValueT]],
        st.SearchStrategy[Order[Sequence[ValueT], tuple[KeyT, ...]]],
    ]:
        def combine_orders(
            orders: Sequence[Order[ValueT, KeyT]], /
        ) -> Order[Sequence[ValueT], tuple[KeyT, ...]]:
            return partial(combine, orders)

        return (
            st.tuples(
                *[
                    value_strategy
                    for value_strategy, _ in values_with_orders_list
                ]
            ),
            st.tuples(
                *[
                    order_strategy
                    for _, order_strategy in values_with_orders_list
                ]
            ).map(combine_orders),
        )

    return st.lists(values_with_orders, max_size=100).map(
        to_values_tuples_with_order
    )


def combine(
    orders: Sequence[Order[ValueT, KeyT]], values: Sequence[ValueT], /
) -> tuple[KeyT, ...]:
    return tuple(
        key(value) for key, value in zip(orders, values, strict=False)
    )


def to_value_with_order_strategy(
    values_with_orders: tuple[
        st.SearchStrategy[Sequence[ValueT]],
        st.SearchStrategy[Order[Sequence[ValueT], tuple[KeyT, ...]]],
    ],
    /,
) -> st.SearchStrategy[
    tuple[Sequence[ValueT], Order[Sequence[ValueT], tuple[KeyT, ...]] | None]
]:
    values, orders = values_with_orders
    return st.tuples(values, st.none() | orders)


def to_value_sequence_with_order_strategy(
    values_with_orders: tuple[
        st.SearchStrategy[ValueT], st.SearchStrategy[Order[ValueT, KeyT]]
    ],
    /,
    *,
    min_size: int,
    max_size: int | None = None,
) -> st.SearchStrategy[ValueSequenceWithOrder[ValueT, KeyT]]:
    values, orders = values_with_orders
    return st.tuples(
        st.lists(values, min_size=min_size, max_size=max_size),
        st.none() | orders,
    )


def to_value_sequences_with_order_strategy(
    values_with_orders: tuple[
        st.SearchStrategy[ValueT], st.SearchStrategy[Order[ValueT, KeyT]]
    ],
    /,
    *,
    sizes: Sequence[tuple[int, int | None]],
) -> st.SearchStrategy[ValueSequencesWithOrder[ValueT, KeyT]]:
    assert len(sizes) > 1, sizes
    values, orders = values_with_orders
    lists_strategies = [
        st.lists(values, min_size=min_size, max_size=max_size)
        for min_size, max_size in sizes
    ]
    return st.tuples(st.tuples(*lists_strategies), st.none() | orders)


def to_non_empty_set_with_their_value_strategy(
    set_: BaseSet[ValueT], /
) -> st.SearchStrategy[tuple[BaseSet[ValueT], ValueT]]:
    return st.tuples(st.just(set_), st.sampled_from(list(set_)))
