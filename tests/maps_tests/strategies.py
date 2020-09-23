from functools import (partial,
                       wraps)
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
from tests.utils import (Map,
                         MapsPair,
                         Strategy,
                         ValuesListWithOrder,
                         ValuesListsWithOrder,
                         has_size_two_or_more)


def to_degenerate_factory(factory: Callable[..., Map]) -> Callable[..., Map]:
    @wraps(factory)
    def wrapper(*items: Item) -> Map:
        result = factory()
        for key, value in items:
            result[key] = value
        return result

    return wrapper


factories = strategies.sampled_from([binary.map_, avl.map_, red_black.map_,
                                     splay.map_])
factories |= factories.map(to_degenerate_factory)


def values_list_with_order_to_items_list(values_list_with_order
                                         : ValuesListWithOrder
                                         ) -> List[Item]:
    values_list, order = values_list_with_order
    return ([(value, value) for value in values_list]
            if order is None
            else [(order(value), value) for value in values_list])


items_lists = (values_lists_with_orders
               .map(values_list_with_order_to_items_list))
single_items = (single_values_with_orders
                .map(values_list_with_order_to_items_list))
non_empty_items_lists = (non_empty_values_lists_with_orders
                         .map(values_list_with_order_to_items_list))
two_or_more_items = (two_or_more_values_with_orders
                     .map(values_list_with_order_to_items_list))


def to_map(factory: Callable[..., Map], items: List[Item]) -> Map:
    return factory(*items)


empty_maps = strategies.builds(to_map, factories, strategies.builds(list))
maps = strategies.builds(to_map, factories, items_lists)
non_empty_maps = strategies.builds(to_map, factories, non_empty_items_lists)
maps_with_two_or_more_items = (strategies.builds(to_map, factories,
                                                 two_or_more_items)
                               .filter(has_size_two_or_more))


def to_map_with_key(factory: Callable[..., Map],
                    items: List[Item]) -> Tuple[Map, Key]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_maps_with_keys = strategies.builds(to_map_with_key, factories,
                                         single_items)
non_empty_maps_with_keys = strategies.builds(to_map_with_key, factories,
                                             two_or_more_items)


def to_map_with_item(factory: Callable[..., Map],
                     items: List[Item]) -> Tuple[Map, Item]:
    *rest_items, item = items
    return factory(*rest_items), item


empty_maps_with_items = strategies.builds(to_map_with_item, factories,
                                          single_items)
maps_with_items = strategies.builds(to_map_with_item, factories,
                                    non_empty_items_lists)
non_empty_maps_with_items = strategies.builds(to_map_with_item, factories,
                                              two_or_more_items)


def to_non_empty_maps_with_their_keys(map_: Map
                                      ) -> Strategy[Tuple[Map, Key]]:
    return strategies.tuples(strategies.just(map_),
                             strategies.sampled_from(list(map_.keys())))


non_empty_maps_with_their_keys = (non_empty_maps
                                  .flatmap(to_non_empty_maps_with_their_keys))


def to_non_empty_maps_with_their_items(map_: Map
                                       ) -> Strategy[Tuple[Map, Item]]:
    return strategies.tuples(strategies.just(map_),
                             strategies.sampled_from(list(map_.items())))


non_empty_maps_with_their_items = (
    non_empty_maps.flatmap(to_non_empty_maps_with_their_items))


def is_key_external(map_with_key: Tuple[Map, Key]) -> bool:
    map_, key = map_with_key
    return key not in map_


non_empty_maps_with_external_keys = (non_empty_maps_with_keys
                                     .filter(is_key_external))


def values_lists_with_order_to_items_lists(values_lists_with_order
                                           : ValuesListsWithOrder
                                           ) -> Tuple[List[Item], ...]:
    *values_lists, order = values_lists_with_order
    return (tuple([(value, value) for value in values_list]
                  for values_list in values_lists)
            if order is None
            else tuple([(order(value), value) for value in values_list]
                       for values_list in values_lists))


def to_map_with_items_list(factory: Callable[..., Map],
                           items_lists_pair: Tuple[List[Item], List[Item]]
                           ) -> Tuple[Map, List[Item]]:
    first_items_list, second_items_list = items_lists_pair
    return factory(*first_items_list), second_items_list


maps_with_items_lists = strategies.builds(
        to_map_with_items_list, factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 2))
         .map(values_lists_with_order_to_items_lists)))


def to_maps_pair(factory: Callable[..., Map],
                 items_lists_pair: Tuple[List[Item], List[Item]]
                 ) -> MapsPair:
    first_items_list, second_items_list = items_lists_pair
    return factory(*first_items_list), factory(*second_items_list)


maps_pairs = strategies.builds(to_maps_pair, factories,
                               values_with_orders_strategies
                               .flatmap(partial(to_values_lists_with_orders,
                                                sizes=[(0, None)] * 2))
                               .map(values_lists_with_order_to_items_lists))
maps_with_items_lists_or_maps = maps_with_items_lists | maps_pairs
