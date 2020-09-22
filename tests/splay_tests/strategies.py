from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import splay
from dendroid.hints import (SortingKey,
                            Value)
from tests.strategies import (non_empty_values_lists_with_keys,
                              to_non_empty_sets_with_their_values,
                              two_or_more_values_with_keys,
                              values_lists_with_keys)
from tests.utils import (Set,
                         ValuesListWithKey)


def to_set(values_list_with_key: Tuple[List[Value], Optional[SortingKey]]
           ) -> Set:
    values_list, key = values_list_with_key
    return splay.set_(*values_list,
                      key=key)


sets = strategies.builds(to_set, values_lists_with_keys)
non_empty_sets = strategies.builds(to_set, non_empty_values_lists_with_keys)
non_empty_sets_with_their_values = (
    non_empty_sets.flatmap(to_non_empty_sets_with_their_values))


def is_value_non_max(set_with_value: Tuple[Set, Value]) -> bool:
    set_, value = set_with_value
    return value != set_.max()


non_empty_sets_with_their_non_max_values = (non_empty_sets_with_their_values
                                            .filter(is_value_non_max))


def is_value_non_min(set_with_value: Tuple[Set, Value]) -> bool:
    tree, value = set_with_value
    return value != tree.min()


non_empty_sets_with_their_non_min_values = (non_empty_sets_with_their_values
                                            .filter(is_value_non_min))


def to_set_with_value(values_list_with_key: ValuesListWithKey
                      ) -> Tuple[Set, Value]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    set_ = splay.set_(*rest_values_list,
                      key=key)
    return set_, value


sets_with_values = strategies.builds(to_set_with_value,
                                     non_empty_values_lists_with_keys)
non_empty_sets_with_values = strategies.builds(to_set_with_value,
                                               two_or_more_values_with_keys)
