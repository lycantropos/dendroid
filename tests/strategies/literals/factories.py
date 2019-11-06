from operator import itemgetter
from typing import List, Optional, Tuple, Sequence

from hypothesis import strategies
from lz.functional import combine, compose

from dendroid.hints import Domain, SortingKey
from tests.utils import Strategy


def to_values_tuples_with_keys(
        values_with_keys: Strategy[Tuple[Strategy[Domain],
                                         Strategy[SortingKey]]]
) -> Strategy[Tuple[Strategy[Tuple[Domain, ...]], Strategy[SortingKey]]]:
    def to_values_tuples_with_key(
            values_with_keys_list: List[Strategy[Tuple[Domain, SortingKey]]]
    ) -> Tuple[Strategy[Tuple[Domain, ...]], Strategy[SortingKey]]:
        def combine_keys(keys: Tuple[SortingKey, ...]) -> SortingKey:
            return compose(tuple, combine(*keys))

        return (strategies.tuples(*map(itemgetter(0), values_with_keys_list)),
                strategies.tuples(*map(itemgetter(1), values_with_keys_list))
                .map(combine_keys))

    return (strategies.lists(values_with_keys,
                             max_size=100)
            .map(to_values_tuples_with_key))


def to_values_with_keys(values_with_keys: Tuple[Strategy[Domain],
                                                Strategy[SortingKey]]
                        ) -> Strategy[Tuple[Domain, Optional[SortingKey]]]:
    values, keys = values_with_keys
    return strategies.tuples(values, strategies.none() | keys)


def to_values_lists_with_keys(
        values_with_keys: Tuple[Strategy[Domain],
                                Strategy[SortingKey]],
        *,
        sizes: Sequence[Tuple[int, Optional[int]]] = ((0, None),)
) -> Strategy[Tuple[List[Domain], Optional[SortingKey]]]:
    values, keys = values_with_keys
    return strategies.tuples(*[strategies.lists(values,
                                                min_size=min_size,
                                                max_size=max_size)
                               for min_size, max_size in sizes],
                             strategies.none() | keys)