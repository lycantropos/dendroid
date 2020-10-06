from functools import partial
from typing import Tuple

from hypothesis import strategies

from dendroid import avl
from dendroid.hints import Value
from tests.strategies import (non_empty_values_lists_with_orders,
                              to_values_lists_with_orders,
                              values_lists_with_orders,
                              values_with_orders_strategies)
from tests.utils import (BaseSet,
                         Strategy,
                         ValuesListWithOrder,
                         ValuesListsPairWithOrder)


def to_set(values_list_with_order: ValuesListWithOrder) -> BaseSet:
    values_list, order = values_list_with_order
    return avl.set_(*values_list,
                    key=order)


sets = strategies.builds(to_set, values_lists_with_orders)
non_empty_sets = strategies.builds(to_set, non_empty_values_lists_with_orders)


def to_set_with_value(values_list_with_order: ValuesListWithOrder
                      ) -> Tuple[BaseSet, Value]:
    values_list, order = values_list_with_order
    *rest_values_list, value = values_list
    return (avl.set_(*rest_values_list,
                     key=order),
            value)


sets_with_values = strategies.builds(to_set_with_value,
                                     non_empty_values_lists_with_orders)


def to_non_empty_sets_with_their_values(set_: BaseSet
                                        ) -> Strategy[Tuple[BaseSet, Value]]:
    return strategies.tuples(strategies.just(set_),
                             strategies.sampled_from(list(set_)))


non_empty_sets_with_their_values = (
    non_empty_sets.flatmap(to_non_empty_sets_with_their_values))


def to_sets_pair(values_lists_pair_with_order: ValuesListsPairWithOrder
                 ) -> Tuple[BaseSet, BaseSet]:
    first_values_list, second_values_list, order = values_lists_pair_with_order
    return (avl.set_(*first_values_list,
                     key=order),
            avl.set_(*second_values_list,
                     key=order))


sets_pairs = strategies.builds(to_sets_pair,
                               values_with_orders_strategies
                               .flatmap(partial(to_values_lists_with_orders,
                                                sizes=[(0, None)] * 2)))
