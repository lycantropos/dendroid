from functools import partial
from typing import (List,
                    Optional,
                    Tuple,
                    Union)

from hypothesis import strategies

from dendroid import red_black
from dendroid.hints import (Domain,
                            SortingKey)
from tests.strategies import (empty_values_lists_with_keys,
                              non_empty_values_lists_with_keys,
                              single_values_with_keys,
                              to_values_lists_with_keys,
                              two_or_more_values_with_keys,
                              values_lists_with_keys,
                              values_with_keys_strategies)
from tests.utils import Strategy


def to_tree(values_list_with_key: Tuple[List[Domain], Optional[SortingKey]]
            ) -> red_black.Tree:
    values_list, key = values_list_with_key
    return red_black.tree(*values_list,
                          key=key)


empty_trees = strategies.builds(to_tree, empty_values_lists_with_keys)
trees = strategies.builds(to_tree, values_lists_with_keys)


def to_empty_tree_with_tree(tree: red_black.Tree
                            ) -> Tuple[red_black.Tree, red_black.Tree]:
    return to_empty_copy(tree), tree


def to_empty_copy(tree: red_black.Tree) -> red_black.Tree:
    return tree.from_iterable((),
                              key=tree.key)


empty_trees_with_trees = trees.map(to_empty_tree_with_tree)
non_empty_trees = strategies.builds(to_tree, non_empty_values_lists_with_keys)


def to_tree_with_value(values_list_with_key: Tuple[List[Domain],
                                                   Optional[SortingKey]]
                       ) -> Tuple[red_black.Tree, Domain]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    tree = red_black.tree(*rest_values_list,
                          key=key)
    return tree, value


trees_with_values = strategies.builds(to_tree_with_value,
                                      non_empty_values_lists_with_keys)
empty_trees_with_values = strategies.builds(to_tree_with_value,
                                            single_values_with_keys)
non_empty_trees_with_values = strategies.builds(to_tree_with_value,
                                                two_or_more_values_with_keys)


def to_non_empty_trees_with_their_values(tree: red_black.Tree
                                         ) -> Strategy[Tuple[red_black.Tree,
                                                             Domain]]:
    return strategies.tuples(strategies.just(tree),
                             strategies.sampled_from(list(tree)))


non_empty_trees_with_their_values = (
    non_empty_trees.flatmap(to_non_empty_trees_with_their_values))


def to_trees_tuple(
        values_lists_with_key: Union[Tuple[List[Domain], Optional[SortingKey]],
                                     Tuple[List[Domain], List[Domain],
                                           Optional[SortingKey]],
                                     Tuple[List[Domain], List[Domain],
                                           List[Domain], Optional[SortingKey]]]
) -> Tuple[red_black.Tree, ...]:
    *values_lists, key = values_lists_with_key
    return tuple(red_black.tree(*values_list,
                                key=key)
                 for values_list in values_lists)


trees_pairs = strategies.builds(to_trees_tuple,
                                values_with_keys_strategies
                                .flatmap(partial(to_values_lists_with_keys,
                                                 sizes=[(0, None)] * 2)))
trees_triplets = strategies.builds(to_trees_tuple,
                                   values_with_keys_strategies
                                   .flatmap(partial(to_values_lists_with_keys,
                                                    sizes=[(0, None)] * 3)))


def to_trees_pair_with_value(
        values_lists_pair_with_key: Tuple[List[Domain], List[Domain],
                                          Optional[SortingKey]]
) -> Tuple[red_black.Tree, red_black.Tree, Domain]:
    first_values_list, second_values_list, key = values_lists_pair_with_key
    *first_values_list, value = first_values_list
    first_tree = red_black.tree(*first_values_list,
                                key=key)
    second_tree = red_black.tree(*second_values_list,
                                 key=key)
    return first_tree, second_tree, value


trees_pairs_with_totally_ordered_values = (
    strategies.builds(to_trees_pair_with_value,
                      values_with_keys_strategies
                      .flatmap(partial(to_values_lists_with_keys,
                                       sizes=[(1, None), (0, None)]))))
