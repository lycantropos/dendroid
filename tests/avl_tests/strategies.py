from functools import partial
from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import avl
from dendroid.hints import (Domain,
                            SortingKey)
from tests.strategies import (non_empty_values_lists_with_keys,
                              to_values_lists_with_keys,
                              values_lists_with_keys,
                              values_with_keys_strategies)
from tests.utils import (Strategy,
                         ValuesListWithKey,
                         ValuesListsPairWithKey)


def to_tree(values_list_with_key: Tuple[List[Domain], Optional[SortingKey]]
            ) -> avl.Tree:
    values_list, key = values_list_with_key
    return avl.tree(*values_list,
                    key=key)


trees = strategies.builds(to_tree, values_lists_with_keys)
non_empty_trees = strategies.builds(to_tree, non_empty_values_lists_with_keys)


def to_tree_with_value(values_list_with_key: ValuesListWithKey
                       ) -> Tuple[avl.Tree, Domain]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    tree = avl.tree(*rest_values_list,
                    key=key)
    return tree, value


trees_with_values = strategies.builds(to_tree_with_value,
                                      non_empty_values_lists_with_keys)


def to_non_empty_trees_with_their_values(tree: avl.Tree
                                         ) -> Strategy[Tuple[avl.Tree,
                                                             Domain]]:
    return strategies.tuples(strategies.just(tree),
                             strategies.sampled_from(list(tree)))


non_empty_trees_with_their_values = (
    non_empty_trees.flatmap(to_non_empty_trees_with_their_values))


def to_trees_pair(values_lists_pair_with_key: ValuesListsPairWithKey
                  ) -> Tuple[avl.Tree, avl.Tree]:
    first_values_lists, second_values_lists, key = values_lists_pair_with_key
    return (avl.tree(*first_values_lists,
                     key=key),
            avl.tree(*second_values_lists,
                     key=key))


trees_pairs = strategies.builds(to_trees_pair,
                                values_with_keys_strategies
                                .flatmap(partial(to_values_lists_with_keys,
                                                 sizes=[(0, None)] * 2)))
