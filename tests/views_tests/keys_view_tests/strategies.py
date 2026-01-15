from collections.abc import Callable, Sequence
from functools import partial
from itertools import starmap
from typing import Any

from hypothesis import strategies

from dendroid import avl, binary, red_black, splay
from dendroid.hints import Item
from tests.hints import KeyT, ValueT
from tests.strategies import (
    non_empty_value_sequence_with_order_strategy,
    single_value_with_order_strategy,
    to_value_sequences_with_order_strategy,
    two_or_more_values_with_order_strategy,
    value_sequence_with_order_strategy,
    value_with_order_strategy_strategy,
)
from tests.utils import (
    KeysView,
    Map,
    ValueSequenceWithOrder,
    ValueSequencesWithOrder,
    compose,
    has_size_two_or_more,
)

factories = strategies.sampled_from(
    [binary.map_, avl.map_, red_black.map_, splay.map_]
).map(partial(compose, Map.keys))


def values_list_with_order_to_items_list(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> list[Item[Any, ValueT]]:
    values_list, order = values_list_with_order
    return (
        [(value, value) for value in values_list]
        if order is None
        else [(order(value), value) for value in values_list]
    )


items_lists = value_sequence_with_order_strategy.map(
    values_list_with_order_to_items_list
)
non_empty_items_lists = non_empty_value_sequence_with_order_strategy.map(
    values_list_with_order_to_items_list
)
single_items = single_value_with_order_strategy.map(
    values_list_with_order_to_items_list
)
two_or_more_items = two_or_more_values_with_order_strategy.map(
    values_list_with_order_to_items_list
)


def to_keys_view(
    factory: Callable[..., KeysView[KeyT]], items: list[Item[KeyT, ValueT]], /
) -> KeysView[KeyT]:
    return factory(*items)


empty_keys_views = strategies.builds(
    to_keys_view, factories, strategies.builds(list)
)
keys_views = strategies.builds(to_keys_view, factories, items_lists)
empty_keys_views_with_keys_views = strategies.tuples(
    empty_keys_views, keys_views
)
non_empty_keys_views = strategies.builds(
    to_keys_view, factories, non_empty_items_lists
)
keys_views_with_two_or_more_values = strategies.builds(
    to_keys_view, factories, two_or_more_items
).filter(has_size_two_or_more)


def to_keys_view_with_key(
    factory: Callable[..., KeysView[KeyT]], items: list[Item[KeyT, ValueT]]
) -> tuple[KeysView[KeyT], KeyT]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_keys_views_with_keys = strategies.builds(
    to_keys_view_with_key, factories, single_items
)


def to_keys_view_with_keys_pair(
    factory: Callable[..., KeysView[KeyT]],
    items_list: list[Item[KeyT, ValueT]],
    /,
) -> tuple[KeysView[KeyT], tuple[KeyT, KeyT]]:
    *rest_items, (first_key, _), (second_key, _) = items_list
    return factory(*rest_items), (first_key, second_key)


keys_views_with_keys_pairs = strategies.builds(
    to_keys_view_with_keys_pair, factories, two_or_more_items
)


def value_sequences_with_order_to_items_lists(
    value_sequences_with_order: ValueSequencesWithOrder[ValueT, KeyT], /
) -> tuple[Sequence[Item[Any, ValueT]], ...]:
    value_sequences, order = value_sequences_with_order
    return (
        tuple(
            [(value, value) for value in values_list]
            for values_list in value_sequences
        )
        if order is None
        else tuple(
            [(order(value), value) for value in values_list]
            for values_list in value_sequences
        )
    )


def to_keys_views_tuple(
    factory: Callable[..., KeysView[KeyT]],
    items_lists: list[list[Item[KeyT, ValueT]]],
    /,
) -> tuple[KeysView[KeyT], ...]:
    return tuple(starmap(factory, items_lists))


keys_views_pairs = strategies.builds(
    to_keys_views_tuple,
    factories,
    (
        value_with_order_strategy_strategy.flatmap(
            partial(
                to_value_sequences_with_order_strategy, sizes=[(0, None)] * 2
            )
        ).map(value_sequences_with_order_to_items_lists)
    ),
)
keys_views_triplets = strategies.builds(
    to_keys_views_tuple,
    factories,
    (
        value_with_order_strategy_strategy.flatmap(
            partial(
                to_value_sequences_with_order_strategy, sizes=[(0, None)] * 3
            )
        ).map(value_sequences_with_order_to_items_lists)
    ),
)


def to_keys_views_pair_with_key(
    factory: Callable[..., KeysView[KeyT]],
    items_lists_pair: tuple[
        list[Item[KeyT, ValueT]], list[Item[KeyT, ValueT]]
    ],
    /,
) -> tuple[KeysView[KeyT], KeysView[KeyT], KeyT]:
    (*first_items, (key, _)), second_items = items_lists_pair
    return factory(*first_items), factory(*second_items), key


keys_views_pairs_with_keys = strategies.builds(
    to_keys_views_pair_with_key,
    factories,
    value_with_order_strategy_strategy.flatmap(
        partial(
            to_value_sequences_with_order_strategy,
            sizes=[(1, None), (0, None)],
        )
    ).map(value_sequences_with_order_to_items_lists),
)
