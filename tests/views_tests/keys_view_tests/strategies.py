from functools import partial
from typing import (Callable,
                    List, Tuple)

from hypothesis import strategies
from lz.functional import compose

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import (Item, Key)
from tests.strategies import (non_empty_values_lists_with_orders,
                              single_values_with_orders,
                              two_or_more_values_with_orders,
                              values_lists_with_orders)
from tests.utils import (KeysView,
                         Map,
                         ValuesListWithOrder)

factories = (strategies.sampled_from([binary.map_, avl.map_, red_black.map_,
                                      splay.map_])
             .map(partial(compose, Map.keys)))


def values_lists_with_orders_to_items_lists(values_list_with_order
                                            : ValuesListWithOrder
                                            ) -> List[Item]:
    values_list, order = values_list_with_order
    return ([(value, value) for value in values_list]
            if order is None
            else [(order(value), value) for value in values_list])


items_lists = (values_lists_with_orders
               .map(values_lists_with_orders_to_items_lists))
non_empty_items_lists = (non_empty_values_lists_with_orders
                         .map(values_lists_with_orders_to_items_lists))
single_items = (single_values_with_orders
                .map(values_lists_with_orders_to_items_lists))
two_or_more_items = (two_or_more_values_with_orders
                     .map(values_lists_with_orders_to_items_lists))


def to_keys_view(factory: Callable[..., KeysView],
                 items: List[Item]) -> KeysView:
    return factory(*items)


empty_keys_views = strategies.builds(to_keys_view, factories,
                                     strategies.builds(list))
keys_views = strategies.builds(to_keys_view, factories, items_lists)
non_empty_keys_views = strategies.builds(to_keys_view, factories,
                                         non_empty_items_lists)


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
