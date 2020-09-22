from functools import partial
from typing import Tuple

from hypothesis import strategies

from dendroid import red_black
from dendroid.hints import Value
from tests.strategies import (non_empty_values_lists_with_keys,
                              to_values_lists_with_keys,
                              values_lists_with_keys,
                              values_with_keys_strategies)
from tests.utils import (Set,
                         Strategy,
                         ValuesListWithKey,
                         ValuesListsPairWithKey)


def to_set(values_list_with_key: ValuesListWithKey) -> Set:
    values_list, key = values_list_with_key
    return red_black.set_(*values_list,
                          key=key)


sets = strategies.builds(to_set, values_lists_with_keys)
non_empty_sets = strategies.builds(to_set, non_empty_values_lists_with_keys)


def to_set_with_value(values_list_with_key: ValuesListWithKey
                      ) -> Tuple[Set, Value]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    set_ = red_black.set_(*rest_values_list,
                          key=key)
    return set_, value


sets_with_values = strategies.builds(to_set_with_value,
                                     non_empty_values_lists_with_keys)


def to_non_empty_sets_with_their_values(set_: Set
                                        ) -> Strategy[Tuple[Set,
                                                            Value]]:
    return strategies.tuples(strategies.just(set_),
                             strategies.sampled_from(list(set_)))


non_empty_sets_with_their_values = (
    non_empty_sets.flatmap(to_non_empty_sets_with_their_values))


def to_sets_pair(values_lists_pair_with_key: ValuesListsPairWithKey
                 ) -> Tuple[Set, Set]:
    first_values_lists, second_values_lists, key = values_lists_pair_with_key
    return (red_black.set_(*first_values_lists,
                           key=key),
            red_black.set_(*second_values_lists,
                           key=key))


sets_pairs = strategies.builds(to_sets_pair,
                               values_with_keys_strategies
                               .flatmap(partial(to_values_lists_with_keys,
                                                sizes=[(0, None)] * 2)))
