from functools import partial
from typing import (Callable,
                    List,
                    Tuple)

from hypothesis import strategies
from lz.functional import compose

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import (Item,
                            Value)
from tests.strategies import (single_values_with_orders,
                              to_values_lists_with_orders,
                              two_or_more_values_with_orders,
                              values_lists_with_orders,
                              values_with_orders_strategies)
from tests.utils import (Map,
                         ValuesListWithOrder,
                         ValuesListsWithOrder,
                         ValuesView, has_size_two_or_more)

factories = (strategies.sampled_from([binary.map_, avl.map_, red_black.map_,
                                      splay.map_])
             .map(partial(compose, Map.values)))


def values_list_with_order_to_items_list(values_list_with_order
                                         : ValuesListWithOrder) -> List[Item]:
    values_list, order = values_list_with_order
    return ([(value, value) for value in values_list]
            if order is None
            else [(order(value), value) for value in values_list])


items_lists = (values_lists_with_orders
               .map(values_list_with_order_to_items_list))
single_items = (single_values_with_orders
                .map(values_list_with_order_to_items_list))
two_or_more_items = (two_or_more_values_with_orders
                     .map(values_list_with_order_to_items_list))


def to_values_view(factory: Callable[..., ValuesView],
                   items: List[Item]) -> ValuesView:
    return factory(*items)


values_views = strategies.builds(to_values_view, factories, items_lists)
values_views_with_two_or_more_values = (strategies.builds(to_values_view,
                                                          factories,
                                                          two_or_more_items)
                                        .filter(has_size_two_or_more))


def to_values_view_with_value(factory: Callable[..., ValuesView],
                              items: List[Item]) -> Tuple[ValuesView, Value]:
    *rest_items, (_, value) = items
    return factory(*rest_items), value


empty_values_views_with_values = strategies.builds(to_values_view_with_value,
                                                   factories, single_items)


def values_lists_with_order_to_items_lists(values_lists_with_order
                                           : ValuesListsWithOrder
                                           ) -> Tuple[List[Item], ...]:
    *values_lists, order = values_lists_with_order
    return (tuple([(value, value) for value in values_list]
                  for values_list in values_lists)
            if order is None
            else tuple([(order(value), value) for value in values_list]
                       for values_list in values_lists))


def to_values_views_tuple(factory: Callable[..., ValuesView],
                          items_lists: List[List[Item]]
                          ) -> Tuple[ValuesView, ...]:
    return tuple(factory(*items_list) for items_list in items_lists)


values_views_pairs = strategies.builds(
        to_values_views_tuple,
        factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 2))
         .map(values_lists_with_order_to_items_lists)))
values_views_triplets = strategies.builds(
        to_values_views_tuple,
        factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 3))
         .map(values_lists_with_order_to_items_lists)))
