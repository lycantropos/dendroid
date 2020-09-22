from functools import (partial,
                       wraps)
from typing import (Callable,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import (SortingKey,
                            Value)
from tests.strategies import (empty_values_lists_with_keys,
                              non_empty_values_lists_with_keys,
                              single_values_with_keys,
                              to_non_empty_sets_with_their_values,
                              to_values_lists_with_keys,
                              two_or_more_values_with_keys,
                              values_lists_with_keys,
                              values_lists_with_none_keys,
                              values_with_keys_strategies)
from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         ValuesListWithKey,
                         ValuesListsPairWithKey,
                         ValuesListsTripletWithKey)


def to_degenerate_factory(factory: Callable[..., Set]) -> Callable[..., Set]:
    @wraps(factory)
    def wrapper(*values: Value,
                key: Optional[SortingKey] = None) -> Set:
        print('degenerate', factory)
        result = factory(key=key)
        for value in values:
            result.add(value)
        return result

    return wrapper


factories = strategies.sampled_from([binary.set_, avl.set_, red_black.set_,
                                     splay.set_])
factories |= factories.map(to_degenerate_factory)


def to_set(factory: Callable[..., Set],
           values_list_with_key: ValuesListWithKey) -> Set:
    values_list, key = values_list_with_key
    return factory(*values_list,
                   key=key)


empty_sets = strategies.builds(to_set, factories, empty_values_lists_with_keys)
sets = strategies.builds(to_set, factories, values_lists_with_keys)
sets_with_none_keys = strategies.builds(to_set, factories,
                                        values_lists_with_none_keys)


def has_three_two_or_more_values(set_: Set) -> bool:
    return len(set_) > 2


sets_with_two_or_more_nodes = (strategies.builds(to_set, factories,
                                                 two_or_more_values_with_keys)
                               .filter(has_three_two_or_more_values))


def to_empty_set_with_set(set_: Set) -> SetsPair:
    return to_empty_copy(set_), set_


def to_empty_copy(set_: Set) -> Set:
    return set_.from_iterable(())


empty_sets_with_sets = sets.map(to_empty_set_with_set)
non_empty_sets = strategies.builds(to_set, factories,
                                   non_empty_values_lists_with_keys)


def to_set_with_value(factory: Callable[..., Set],
                      values_list_with_key: ValuesListWithKey
                      ) -> Tuple[Set, Value]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    set_ = factory(*rest_values_list,
                   key=key)
    return set_, value


sets_with_values = strategies.builds(to_set_with_value, factories,
                                     non_empty_values_lists_with_keys)
empty_sets_with_values = strategies.builds(to_set_with_value, factories,
                                           single_values_with_keys)
non_empty_sets_with_values = strategies.builds(to_set_with_value, factories,
                                               two_or_more_values_with_keys)


def is_value_external(set_with_value: Tuple[Set, Value]) -> bool:
    set_, value = set_with_value
    return value not in set_


non_empty_sets_with_external_values = (non_empty_sets_with_values
                                       .filter(is_value_external))


def to_set_with_values_pair(factory: Callable[..., Set],
                            values_list_with_key: ValuesListWithKey
                            ) -> Tuple[Set, Tuple[Value, Value]]:
    values_list, key = values_list_with_key
    *rest_values_list, first_value, second_value = values_list
    set_ = factory(*rest_values_list,
                   key=key)
    return set_, (first_value, second_value)


sets_with_values_pairs = strategies.builds(to_set_with_values_pair,
                                           factories,
                                           two_or_more_values_with_keys)
non_empty_sets_with_their_values = (
    non_empty_sets.flatmap(to_non_empty_sets_with_their_values))


def to_sets_pair(factory: Callable[..., Set],
                 values_lists_pair_with_key: ValuesListsPairWithKey
                 ) -> SetsPair:
    first_values_list, second_values_list, key = values_lists_pair_with_key
    first_set = factory(*first_values_list,
                        key=key)
    second_set = factory(*second_values_list,
                         key=key)
    return first_set, second_set


sets_pairs = strategies.builds(to_sets_pair,
                               factories,
                               values_with_keys_strategies
                               .flatmap(partial(to_values_lists_with_keys,
                                                sizes=[(0, None)] * 2)))


def to_sets_triplet(factory: Callable[..., Set],
                    values_lists_triplet_with_key: ValuesListsTripletWithKey
                    ) -> SetsTriplet:
    (first_values_list, second_values_list,
     third_values_list, key) = values_lists_triplet_with_key
    first_set = factory(*first_values_list,
                        key=key)
    second_set = factory(*second_values_list,
                         key=key)
    third_set = factory(*third_values_list,
                        key=key)
    return first_set, second_set, third_set


sets_triplets = strategies.builds(to_sets_triplet, factories,
                                  (values_with_keys_strategies
                                   .flatmap(partial(to_values_lists_with_keys,
                                                    sizes=[(0, None)] * 3))))


def to_sets_pair_with_value(factory: Callable[..., Set],
                            values_lists_pair_with_key: ValuesListsPairWithKey
                            ) -> Tuple[Set, Set, Value]:
    first_values_list, second_values_list, key = values_lists_pair_with_key
    *first_values_list, value = first_values_list
    first_set = factory(*first_values_list,
                        key=key)
    second_set = factory(*second_values_list,
                         key=key)
    return first_set, second_set, value


sets_pairs_with_values = (
    strategies.builds(to_sets_pair_with_value,
                      factories,
                      values_with_keys_strategies
                      .flatmap(partial(to_values_lists_with_keys,
                                       sizes=[(1, None), (0, None)]))))
