from functools import partial

from hypothesis import strategies
from lz.functional import identity

totally_ordered_values_strategies = (
    strategies.sampled_from([strategies.integers(),
                             strategies.floats(allow_nan=False),
                             strategies.booleans(),
                             strategies.text()]))
totally_ordered_values = totally_ordered_values_strategies.flatmap(identity)
totally_ordered_values_lists = (totally_ordered_values_strategies
                                .flatmap(strategies.lists))
non_empty_totally_ordered_values_lists = (totally_ordered_values_strategies
                                          .flatmap(partial(strategies.lists,
                                                           min_size=1)))
keys = strategies.sampled_from([identity, None])
