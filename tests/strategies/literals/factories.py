from functools import partial
from operator import itemgetter
from typing import (List,
                    Optional,
                    Sequence,
                    Tuple,
                    Union)

from hypothesis import strategies

from dendroid.hints import (Domain,
                            Sortable,
                            SortingKey)
from tests.utils import (Strategy,
                         Tree,
                         ValuesListWithKey,
                         ValuesListsPairWithKey,
                         ValuesListsTripletWithKey)


def to_values_tuples_with_keys(
        values_with_keys: Strategy[Tuple[Strategy[Domain],
                                         Strategy[SortingKey]]]
) -> Strategy[Tuple[Strategy[Tuple[Domain, ...]], Strategy[SortingKey]]]:
    def to_values_tuples_with_key(
            values_with_keys_list: List[Strategy[Tuple[Domain, SortingKey]]]
    ) -> Tuple[Strategy[Tuple[Domain, ...]], Strategy[SortingKey]]:
        def combine_keys(keys: Tuple[SortingKey, ...]) -> SortingKey:
            return partial(combine, keys)

        return (strategies.tuples(*map(itemgetter(0), values_with_keys_list)),
                strategies.tuples(*map(itemgetter(1), values_with_keys_list))
                .map(combine_keys))

    return (strategies.lists(values_with_keys,
                             max_size=100)
            .map(to_values_tuples_with_key))


def combine(keys: Sequence[SortingKey],
            values: Sequence[Domain]) -> Tuple[Sortable, ...]:
    return tuple(key(value) for key, value in zip(keys, values))


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
) -> Strategy[Union[ValuesListWithKey,
                    ValuesListsPairWithKey,
                    ValuesListsTripletWithKey]]:
    values, keys = values_with_keys
    lists_strategies = [strategies.lists(values,
                                         min_size=min_size,
                                         max_size=max_size)
                        for min_size, max_size in sizes]
    return strategies.tuples(*lists_strategies, strategies.none() | keys)


def to_non_empty_trees_with_their_values(tree: Tree
                                         ) -> Strategy[Tuple[Tree, Domain]]:
    return strategies.tuples(strategies.just(tree),
                             strategies.sampled_from(list(tree)))
