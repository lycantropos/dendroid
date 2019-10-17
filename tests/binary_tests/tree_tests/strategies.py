from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import binary
from dendroid.hints import (Domain,
                            SortingKey)
from tests.strategies import (keys,
                              non_empty_totally_ordered_values,
                              totally_ordered_values,
                              totally_ordered_values_lists)

totally_ordered_values = totally_ordered_values
empty_trees = strategies.builds(binary.tree,
                                key=keys)


def to_tree(values_list_with_key: Tuple[List[Domain], Optional[SortingKey]]
            ) -> binary.Tree:
    values_list, key = values_list_with_key
    return binary.tree(*values_list,
                       key=key)


trees = strategies.tuples(totally_ordered_values_lists, keys).map(to_tree)


def to_tree_with_totally_ordered_value(
        values_list_with_key: Tuple[List[Domain], Optional[SortingKey]]
) -> Tuple[binary.Tree, Domain]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    tree = binary.tree(*rest_values_list,
                       key=key)
    return tree, value


trees_with_totally_ordered_values = (
    strategies.tuples(non_empty_totally_ordered_values,
                      keys).map(to_tree_with_totally_ordered_value))
