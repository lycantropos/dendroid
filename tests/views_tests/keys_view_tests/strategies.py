from functools import partial
from typing import (Callable,
                    List,
                    Tuple)

from hypothesis import strategies

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import (Item,
                            Key)
from tests.strategies import (non_empty_values_lists_with_orders,
                              single_values_with_orders,
                              to_values_lists_with_orders,
                              two_or_more_values_with_orders,
                              values_lists_with_orders,
                              values_with_orders_strategies)
from tests.utils import (KeysView,
                         Map,
                         ValuesListWithOrder,
                         ValuesListsWithOrder,
                         compose,
                         has_size_two_or_more)

factories = (strategies.sampled_from([binary.map_, avl.map_, red_black.map_,
                                      splay.map_])
             .map(partial(compose, Map.keys)))


def values_list_with_order_to_items_list(values_list_with_order
                                         : ValuesListWithOrder) -> List[Item]:
    values_list, order = values_list_with_order
    return ([(value, value) for value in values_list]
            if order is None
            else [(order(value), value) for value in values_list])


items_lists = (values_lists_with_orders
               .map(values_list_with_order_to_items_list))
non_empty_items_lists = (non_empty_values_lists_with_orders
                         .map(values_list_with_order_to_items_list))
single_items = (single_values_with_orders
                .map(values_list_with_order_to_items_list))
two_or_more_items = (two_or_more_values_with_orders
                     .map(values_list_with_order_to_items_list))


def to_keys_view(factory: Callable[..., KeysView],
                 items: List[Item]) -> KeysView:
    return factory(*items)


empty_keys_views = strategies.builds(to_keys_view, factories,
                                     strategies.builds(list))
keys_views = strategies.builds(to_keys_view, factories, items_lists)
empty_keys_views_with_keys_views = strategies.tuples(empty_keys_views,
                                                     keys_views)
non_empty_keys_views = strategies.builds(to_keys_view, factories,
                                         non_empty_items_lists)
keys_views_with_two_or_more_values = (strategies.builds(to_keys_view,
                                                        factories,
                                                        two_or_more_items)
                                      .filter(has_size_two_or_more))


def to_keys_view_with_key(factory: Callable[..., KeysView],
                          items: List[Item]) -> Tuple[KeysView, Key]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_keys_views_with_keys = strategies.builds(to_keys_view_with_key,
                                               factories, single_items)


def to_keys_view_with_keys_pair(factory: Callable[..., KeysView],
                                items_list: List[Item]
                                ) -> Tuple[KeysView, Tuple[Key, Key]]:
    *rest_items, (first_key, _), (second_key, _) = items_list
    return factory(*rest_items), (first_key, second_key)


keys_views_with_keys_pairs = strategies.builds(to_keys_view_with_keys_pair,
                                               factories, two_or_more_items)


def values_lists_with_order_to_items_lists(values_lists_with_order
                                           : ValuesListsWithOrder
                                           ) -> Tuple[List[Item], ...]:
    *values_lists, order = values_lists_with_order
    return (tuple([(value, value) for value in values_list]
                  for values_list in values_lists)
            if order is None
            else tuple([(order(value), value) for value in values_list]
                       for values_list in values_lists))


def to_keys_views_tuple(factory: Callable[..., KeysView],
                        items_lists: List[List[Item]]) -> Tuple[KeysView, ...]:
    return tuple(factory(*items_list) for items_list in items_lists)


keys_views_pairs = strategies.builds(
        to_keys_views_tuple,
        factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 2))
         .map(values_lists_with_order_to_items_lists)))
keys_views_triplets = strategies.builds(
        to_keys_views_tuple,
        factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 3))
         .map(values_lists_with_order_to_items_lists)))


def to_keys_views_pair_with_key(factory: Callable[..., KeysView],
                                items_lists_pair: Tuple[List[Item], List[Item]]
                                ) -> Tuple[KeysView, KeysView, Key]:
    (*first_items, (key, _)), second_items = items_lists_pair
    return factory(*first_items), factory(*second_items), key


keys_views_pairs_with_keys = (
    strategies.builds(to_keys_views_pair_with_key,
                      factories,
                      values_with_orders_strategies
                      .flatmap(partial(to_values_lists_with_orders,
                                       sizes=[(1, None), (0, None)]))
                      .map(values_lists_with_order_to_items_lists)))
