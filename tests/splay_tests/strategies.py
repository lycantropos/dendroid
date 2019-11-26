from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import splay
from dendroid.hints import (Domain,
                            SortingKey)
from tests.strategies import (non_empty_values_lists_with_keys,
                              to_non_empty_trees_with_their_values,
                              two_or_more_values_with_keys)
from tests.utils import (ValuesListWithKey)


def to_tree(values_list_with_key: Tuple[List[Domain], Optional[SortingKey]]
            ) -> splay.Tree:
    values_list, key = values_list_with_key
    return splay.tree(*values_list,
                      key=key)


non_empty_trees = strategies.builds(to_tree, non_empty_values_lists_with_keys)
non_empty_trees_with_their_values = (
    non_empty_trees.flatmap(to_non_empty_trees_with_their_values))


def is_value_non_max(tree_with_value: Tuple[splay.Tree, Domain]) -> bool:
    tree, value = tree_with_value
    return value != tree.max()


non_empty_trees_with_their_non_max_values = (non_empty_trees_with_their_values
                                             .filter(is_value_non_max))


def to_tree_with_value(values_list_with_key: ValuesListWithKey
                       ) -> Tuple[splay.Tree, Domain]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    tree = splay.tree(*rest_values_list,
                      key=key)
    return tree, value


trees_with_values = strategies.builds(to_tree_with_value,
                                      non_empty_values_lists_with_keys)
non_empty_trees_with_values = strategies.builds(to_tree_with_value,
                                                two_or_more_values_with_keys)
