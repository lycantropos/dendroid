from functools import (partial,
                       wraps)
from typing import (Callable,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import (Order,
                            Value)
from tests.strategies import (empty_values_lists_with_orders,
                              non_empty_values_lists_with_orders,
                              single_values_with_orders,
                              to_non_empty_sets_with_their_values,
                              to_values_lists_with_orders,
                              two_or_more_values_with_orders,
                              values_lists_with_none_orders,
                              values_lists_with_orders,
                              values_with_orders_strategies)
from tests.utils import (Set,
                         SetsPair,
                         ValuesListWithOrder,
                         ValuesListsPairWithOrder)


def to_degenerate_factory(factory: Callable[..., Set]) -> Callable[..., Set]:
    @wraps(factory)
    def wrapper(*values: Value,
                key: Optional[Order] = None) -> Set:
        result = factory(key=key)
        for value in values:
            result.add(value)
        return result

    return wrapper


factories = strategies.sampled_from([binary.set_, avl.set_, red_black.set_,
                                     splay.set_])
factories |= factories.map(to_degenerate_factory)


def to_set(factory: Callable[..., Set],
           values_list_with_order: ValuesListWithOrder) -> Set:
    values_list, order = values_list_with_order
    return factory(*values_list,
                   key=order)


empty_sets = strategies.builds(to_set, factories,
                               empty_values_lists_with_orders)
sets = strategies.builds(to_set, factories, values_lists_with_orders)
sets_with_none_orders = strategies.builds(to_set, factories,
                                          values_lists_with_none_orders)


def set_has_two_or_more_values(set_: Set) -> bool:
    return len(set_) >= 2


sets_with_two_or_more_values = (
    (strategies.builds(to_set, factories, two_or_more_values_with_orders)
     .filter(set_has_two_or_more_values)))


def to_empty_set_with_set(set_: Set) -> SetsPair:
    return to_empty_copy(set_), set_


def to_empty_copy(set_: Set) -> Set:
    return set_.from_iterable(())


empty_sets_with_sets = sets.map(to_empty_set_with_set)
non_empty_sets = strategies.builds(to_set, factories,
                                   non_empty_values_lists_with_orders)


def to_set_with_value(factory: Callable[..., Set],
                      values_list_with_order: ValuesListWithOrder
                      ) -> Tuple[Set, Value]:
    values_list, order = values_list_with_order
    *rest_values_list, value = values_list
    set_ = factory(*rest_values_list,
                   key=order)
    return set_, value


sets_with_values = strategies.builds(to_set_with_value, factories,
                                     non_empty_values_lists_with_orders)
empty_sets_with_values = strategies.builds(to_set_with_value, factories,
                                           single_values_with_orders)
non_empty_sets_with_values = strategies.builds(to_set_with_value, factories,
                                               two_or_more_values_with_orders)


def is_value_external(set_with_value: Tuple[Set, Value]) -> bool:
    set_, value = set_with_value
    return value not in set_


non_empty_sets_with_external_values = (non_empty_sets_with_values
                                       .filter(is_value_external))


def to_set_with_values_pair(factory: Callable[..., Set],
                            values_list_with_order: ValuesListWithOrder
                            ) -> Tuple[Set, Tuple[Value, Value]]:
    values_list, order = values_list_with_order
    *rest_values_list, first_value, second_value = values_list
    set_ = factory(*rest_values_list,
                   key=order)
    return set_, (first_value, second_value)


sets_with_values_pairs = strategies.builds(to_set_with_values_pair,
                                           factories,
                                           two_or_more_values_with_orders)
non_empty_sets_with_their_values = (
    non_empty_sets.flatmap(to_non_empty_sets_with_their_values))


def to_sets_tuple(factory: Callable[..., Set],
                  values_lists_pair_with_order: ValuesListsPairWithOrder
                  ) -> Tuple[Set, ...]:
    *values_lists, order = values_lists_pair_with_order
    return tuple(factory(*values_list,
                         key=order)
                 for values_list in values_lists)


sets_pairs = strategies.builds(to_sets_tuple,
                               factories,
                               values_with_orders_strategies
                               .flatmap(partial(to_values_lists_with_orders,
                                                sizes=[(0, None)] * 2)))
sets_triplets = strategies.builds(
        to_sets_tuple, factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 3))))


def to_sets_pair_with_value(factory: Callable[..., Set],
                            values_lists_pair_with_order
                            : ValuesListsPairWithOrder
                            ) -> Tuple[Set, Set, Value]:
    first_values, second_values, order = values_lists_pair_with_order
    *first_values, value = first_values
    first_set = factory(*first_values,
                        key=order)
    second_set = factory(*second_values,
                         key=order)
    return first_set, second_set, value


sets_pairs_with_values = (
    strategies.builds(to_sets_pair_with_value,
                      factories,
                      values_with_orders_strategies
                      .flatmap(partial(to_values_lists_with_orders,
                                       sizes=[(1, None), (0, None)]))))
