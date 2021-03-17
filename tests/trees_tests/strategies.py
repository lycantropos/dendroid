from functools import partial
from operator import attrgetter
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
from tests.utils import (Node,
                         Strategy,
                         Tree,
                         ValuesListWithOrder,
                         ValuesListsWithOrder,
                         compose,
                         has_size_two_or_more)

factories = (strategies.sampled_from([binary.map_, avl.map_, red_black.map_,
                                      splay.map_])
             .map(partial(compose, attrgetter('tree'))))


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


def to_tree(factory: Callable[..., Tree], items: List[Item]) -> Tree:
    return factory(*items)


empty_trees = strategies.builds(to_tree, factories,
                                strategies.builds(list))
trees = strategies.builds(to_tree, factories, items_lists)
non_empty_trees = strategies.builds(to_tree, factories,
                                    non_empty_items_lists)
trees_with_two_or_more_nodes = (strategies.builds(to_tree, factories,
                                                  two_or_more_items)
                                .filter(has_size_two_or_more))


def to_tree_with_key(factory: Callable[..., Tree],
                     items: List[Item]) -> Tuple[Tree, Key]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_trees_with_keys = strategies.builds(to_tree_with_key,
                                          factories, single_items)
trees_with_keys = strategies.builds(to_tree_with_key, factories,
                                    non_empty_items_lists)


def to_non_empty_trees_with_their_keys(tree: Tree
                                       ) -> Strategy[Tuple[Tree, Key]]:
    return strategies.tuples(strategies.just(tree),
                             strategies.sampled_from(tree.keys))


non_empty_trees_with_their_keys = (
    non_empty_trees.flatmap(to_non_empty_trees_with_their_keys))


def to_non_empty_trees_with_their_nodes(tree: Tree
                                        ) -> Strategy[Tuple[Tree, Node]]:
    return strategies.tuples(strategies.just(tree),
                             strategies.sampled_from(list(tree)))


non_empty_trees_with_their_nodes = (
    non_empty_trees.flatmap(to_non_empty_trees_with_their_nodes))


def values_lists_with_order_to_items_lists(values_lists_with_order
                                           : ValuesListsWithOrder
                                           ) -> Tuple[List[Item], ...]:
    *values_lists, order = values_lists_with_order
    return (tuple([(value, value) for value in values_list]
                  for values_list in values_lists)
            if order is None
            else tuple([(order(value), value) for value in values_list]
                       for values_list in values_lists))


def to_trees_tuple(factory: Callable[..., Tree],
                   items_lists: List[List[Item]]
                   ) -> Tuple[Tree, ...]:
    return tuple(factory(*items_list) for items_list in items_lists)


trees_pairs = strategies.builds(
        to_trees_tuple,
        factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 2))
         .map(values_lists_with_order_to_items_lists)))
trees_triplets = strategies.builds(
        to_trees_tuple,
        factories,
        (values_with_orders_strategies
         .flatmap(partial(to_values_lists_with_orders,
                          sizes=[(0, None)] * 3))
         .map(values_lists_with_order_to_items_lists)))
