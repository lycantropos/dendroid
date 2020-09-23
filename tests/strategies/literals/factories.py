from functools import partial
from operator import itemgetter
from typing import (List,
                    Optional,
                    Sequence,
                    Tuple)

from hypothesis import strategies

from dendroid.hints import (Key,
                            Order,
                            Value)
from tests.utils import (Set,
                         Strategy,
                         ValuesListsWithOrder)


def to_values_tuples_with_orders(
        values_with_orders: Strategy[Tuple[Strategy[Value], Strategy[Order]]]
) -> Strategy[Tuple[Strategy[Tuple[Value, ...]], Strategy[Order]]]:
    def to_values_tuples_with_order(values_with_orders_list
                                    : List[Strategy[Tuple[Value, Order]]]
                                    ) -> Tuple[Strategy[Tuple[Value, ...]],
                                               Strategy[Order]]:
        def combine_orders(orders: Tuple[Order, ...]) -> Order:
            return partial(combine, orders)

        return (strategies.tuples(*map(itemgetter(0),
                                       values_with_orders_list)),
                strategies.tuples(*map(itemgetter(1), values_with_orders_list))
                .map(combine_orders))

    return (strategies.lists(values_with_orders,
                             max_size=100)
            .map(to_values_tuples_with_order))


def combine(orders: Sequence[Order],
            values: Sequence[Value]) -> Tuple[Key, ...]:
    return tuple(key(value) for key, value in zip(orders, values))


def to_values_with_orders(values_with_orders: Tuple[Strategy[Value],
                                                    Strategy[Order]]
                          ) -> Strategy[Tuple[Value, Optional[Order]]]:
    values, orders = values_with_orders
    return strategies.tuples(values, strategies.none() | orders)


def to_values_lists_with_orders(
        values_with_orders
        : Tuple[Strategy[Value], Strategy[Order]],
        *,
        sizes: Sequence[Tuple[int, Optional[int]]] = ((0, None),)
) -> Strategy[ValuesListsWithOrder]:
    values, orders = values_with_orders
    lists_strategies = [strategies.lists(values,
                                         min_size=min_size,
                                         max_size=max_size)
                        for min_size, max_size in sizes]
    return strategies.tuples(*lists_strategies, strategies.none() | orders)


def to_non_empty_sets_with_their_values(set_: Set
                                        ) -> Strategy[Tuple[Set, Value]]:
    return strategies.tuples(strategies.just(set_),
                             strategies.sampled_from(list(set_)))
