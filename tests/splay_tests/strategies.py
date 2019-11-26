from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import splay
from dendroid.hints import (Domain,
                            SortingKey)
from tests.strategies import (non_empty_values_lists_with_keys,
                              two_or_more_values_with_keys)
from tests.utils import (ValuesListWithKey)


def to_tree(values_list_with_key: Tuple[List[Domain], Optional[SortingKey]]
            ) -> splay.Tree:
    values_list, key = values_list_with_key
    return splay.tree(*values_list,
                      key=key)


non_empty_trees = strategies.builds(to_tree, non_empty_values_lists_with_keys)


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
