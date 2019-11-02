from functools import partial
from typing import Optional

from hypothesis import strategies
from lz.functional import (identity,
                           pack)

from dendroid.hints import Sortable
from tests.utils import Strategy

totally_ordered_values_strategies = (
    strategies.sampled_from([strategies.integers(),
                             strategies.floats(allow_nan=False),
                             strategies.booleans(),
                             strategies.text()]))
totally_ordered_values_strategies |= (
    strategies.lists(totally_ordered_values_strategies,
                     max_size=100).map(pack(strategies.tuples)))
totally_ordered_values = totally_ordered_values_strategies.flatmap(identity)
totally_ordered_values_lists = (totally_ordered_values_strategies
                                .flatmap(strategies.lists))


def to_totally_ordered_values_lists(*,
                                    min_size=0,
                                    max_size: Optional[int] = None
                                    ) -> Strategy[Sortable]:
    return (totally_ordered_values_strategies
            .flatmap(partial(strategies.lists,
                             min_size=min_size,
                             max_size=max_size)))


non_empty_totally_ordered_values_lists = to_totally_ordered_values_lists(
        min_size=1)
keys = strategies.sampled_from([identity, None])
