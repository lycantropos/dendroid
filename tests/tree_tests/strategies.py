from functools import partial
from typing import (Callable,
                    List,
                    Optional,
                    Tuple,
                    TypeVar)

from hypothesis import strategies

from dendroid import binary, red_black
from dendroid.hints import (Domain,
                            SortingKey)
from tests.strategies import (keys,
                              non_empty_totally_ordered_values_lists,
                              to_totally_ordered_values_lists,
                              totally_ordered_values,
                              totally_ordered_values_lists,
                              totally_ordered_values_strategies)
from tests.utils import (Strategy,
                         builds_from)

totally_ordered_values = totally_ordered_values
factories = strategies.sampled_from([binary.tree, red_black.tree])
packed_factories = strategies.sampled_from([binary.Tree.from_iterable,
                                            red_black.Tree.from_iterable])

empty_trees = builds_from(factories,
                          key=keys)
trees = builds_from(packed_factories,
                    totally_ordered_values_lists,
                    key=keys)
non_empty_trees = builds_from(packed_factories,
                              non_empty_totally_ordered_values_lists,
                              key=keys)

Tree = TypeVar('Tree', binary.Tree, red_black.Tree)


def to_tree_with_totally_ordered_value(factory: Callable[..., Tree],
                                       values_list: List[Domain],
                                       key: Optional[SortingKey]
                                       ) -> Tuple[Tree, Domain]:
    *rest_values_list, value = values_list
    tree = factory(*rest_values_list,
                   key=key)
    return tree, value


trees_with_totally_ordered_values = strategies.builds(
        to_tree_with_totally_ordered_value,
        factories,
        non_empty_totally_ordered_values_lists,
        keys)
non_empty_trees_with_totally_ordered_values = strategies.builds(
        to_tree_with_totally_ordered_value,
        factories,
        to_totally_ordered_values_lists(min_size=2),
        keys)


def to_trees_pair(factory: Callable[..., Tree],
                  values_lists_pair: Tuple[List[Domain], List[Domain]],
                  key: Optional[SortingKey]) -> Tuple[Tree, Tree]:
    first_values_list, second_values_list = values_lists_pair
    first_tree = factory(*first_values_list,
                         key=key)
    second_tree = factory(*second_values_list,
                          key=key)
    return first_tree, second_tree


def to_values_lists_pairs(values: Strategy[Domain],
                          *,
                          first_min_size: int = 0,
                          first_max_size: Optional[int] = None,
                          second_min_size: int = 0,
                          second_max_size: Optional[int] = None
                          ) -> Strategy[Tuple[List[Domain], List[Domain]]]:
    return strategies.tuples(strategies.lists(values,
                                              min_size=first_min_size,
                                              max_size=first_max_size),
                             strategies.lists(values,
                                              min_size=second_min_size,
                                              max_size=second_max_size))


trees_pairs = strategies.builds(to_trees_pair,
                                factories,
                                totally_ordered_values_strategies
                                .flatmap(to_values_lists_pairs),
                                keys)


def to_trees_triplet(factory: Callable[..., Tree],
                     values_lists_triplet: Tuple[List[Domain], List[Domain],
                                                 List[Domain]],
                     key: Optional[SortingKey]) -> Tuple[Tree, Tree, Tree]:
    (first_values_list, second_values_list,
     third_values_list) = values_lists_triplet
    first_tree = factory(*first_values_list,
                         key=key)
    second_tree = factory(*second_values_list,
                          key=key)
    third_tree = factory(*third_values_list,
                         key=key)
    return first_tree, second_tree, third_tree


def to_values_lists_triplets(values: Strategy[Domain],
                             *,
                             first_min_size: int = 0,
                             first_max_size: Optional[int] = None,
                             second_min_size: int = 0,
                             second_max_size: Optional[int] = None,
                             third_min_size: int = 0,
                             third_max_size: Optional[int] = None
                             ) -> Strategy[Tuple[List[Domain], List[Domain]]]:
    return strategies.tuples(strategies.lists(values,
                                              min_size=first_min_size,
                                              max_size=first_max_size),
                             strategies.lists(values,
                                              min_size=second_min_size,
                                              max_size=second_max_size),
                             strategies.lists(values,
                                              min_size=third_min_size,
                                              max_size=third_max_size))


trees_triplets = strategies.builds(to_trees_triplet,
                                   factories,
                                   totally_ordered_values_strategies
                                   .flatmap(to_values_lists_triplets),
                                   keys)


def to_trees_pair_with_totally_ordered_value(
        factory: Callable[..., Tree],
        values_lists_pair: Tuple[List[Domain], List[Domain]],
        key: Optional[SortingKey]) -> Tuple[Tree, Tree, Domain]:
    first_values_list, second_values_list = values_lists_pair
    *first_values_list, value = first_values_list
    first_tree = factory(*first_values_list,
                         key=key)
    second_tree = factory(*second_values_list,
                          key=key)
    return first_tree, second_tree, value


trees_pairs_with_totally_ordered_values = (
    strategies.builds(to_trees_pair_with_totally_ordered_value,
                      factories,
                      totally_ordered_values_strategies
                      .flatmap(partial(to_values_lists_pairs,
                                       first_min_size=1)),
                      keys))
