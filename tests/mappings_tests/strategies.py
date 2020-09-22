from functools import wraps
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
                              two_or_more_values_with_orders,
                              values_lists_with_orders)
from tests.utils import (Map,
                         Strategy,
                         ValuesListWithOrder)


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


def values_lists_with_orders_to_items_lists(values_list_with_order
                                            : ValuesListWithOrder
                                            ) -> List[Item]:
    values_list, order = values_list_with_order
    return ([(value, value) for value in values_list]
            if order is None
            else [(order(value), value) for value in values_list])


items_lists = (values_lists_with_orders
               .map(values_lists_with_orders_to_items_lists))
single_items = (single_values_with_orders
                .map(values_lists_with_orders_to_items_lists))
non_empty_items_lists = (non_empty_values_lists_with_orders
                         .map(values_lists_with_orders_to_items_lists))
two_or_more_items = (two_or_more_values_with_orders
                     .map(values_lists_with_orders_to_items_lists))


def to_map(factory: Callable[..., Map], items: ValuesListWithOrder) -> Map:
    return factory(*items)


empty_maps = strategies.builds(to_map, factories, strategies.builds(list))
maps = strategies.builds(to_map, factories, items_lists)
non_empty_maps = strategies.builds(to_map, factories, non_empty_items_lists)


def map_has_two_or_more_items(map_: Map) -> bool:
    return len(map_) >= 2


maps_with_two_or_more_items = (strategies.builds(to_map, factories,
                                                 two_or_more_items)
                               .filter(map_has_two_or_more_items))


def to_map_with_key(factory: Callable[..., Map],
                    items: List[Item]) -> Tuple[Map, Key]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_maps_with_keys = strategies.builds(to_map_with_key, factories,
                                         single_items)


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
                             strategies.sampled_from(list(map_)))


non_empty_maps_with_their_keys = (non_empty_maps
                                  .flatmap(to_non_empty_maps_with_their_keys))
