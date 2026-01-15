from collections.abc import Callable, Sequence
from functools import partial, wraps
from typing import Any

from hypothesis import strategies as st

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
    Map,
    MapsPair,
    ValueSequenceWithOrder,
    ValueSequencesWithOrder,
    has_size_two_or_more,
)


def to_degenerate_factory(
    factory: Callable[..., Map[KeyT, ValueT]], /
) -> Callable[..., Map[KeyT, ValueT]]:
    @wraps(factory)
    def wrapper(*items: Item[KeyT, ValueT]) -> Map[KeyT, ValueT]:
        result = factory()
        for key, value in items:
            result[key] = value
        return result

    return wrapper


factories = st.sampled_from(
    [binary.map_, avl.map_, red_black.map_, splay.map_]
)
factories |= factories.map(to_degenerate_factory)


def values_list_with_order_to_items_list(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> Sequence[Item[Any, ValueT]]:
    values_list, order = values_list_with_order
    return (
        [(value, value) for value in values_list]
        if order is None
        else [(order(value), value) for value in values_list]
    )


items_lists = value_sequence_with_order_strategy.map(
    values_list_with_order_to_items_list
)
single_items = single_value_with_order_strategy.map(
    values_list_with_order_to_items_list
)
non_empty_items_lists = non_empty_value_sequence_with_order_strategy.map(
    values_list_with_order_to_items_list
)
two_or_more_items = two_or_more_values_with_order_strategy.map(
    values_list_with_order_to_items_list
)


def to_map(
    factory: Callable[..., Map[KeyT, ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> Map[KeyT, ValueT]:
    return factory(*items)


empty_maps = st.builds(to_map, factories, st.builds(list))
maps = st.builds(to_map, factories, items_lists)
non_empty_maps = st.builds(to_map, factories, non_empty_items_lists)
maps_with_two_or_more_items = st.builds(
    to_map, factories, two_or_more_items
).filter(has_size_two_or_more)


def to_map_with_key(
    factory: Callable[..., Map[KeyT, ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> tuple[Map[KeyT, ValueT], KeyT]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_maps_with_keys = st.builds(to_map_with_key, factories, single_items)
non_empty_maps_with_keys = st.builds(
    to_map_with_key, factories, two_or_more_items
)


def to_map_with_item(
    factory: Callable[..., Map[KeyT, ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> tuple[Map[KeyT, ValueT], Item[KeyT, ValueT]]:
    *rest_items, item = items
    return factory(*rest_items), item


empty_maps_with_items = st.builds(to_map_with_item, factories, single_items)
maps_with_items = st.builds(to_map_with_item, factories, non_empty_items_lists)
non_empty_maps_with_items = st.builds(
    to_map_with_item, factories, two_or_more_items
)


def to_non_empty_maps_with_their_keys(
    map_: Map[KeyT, ValueT], /
) -> st.SearchStrategy[tuple[Map[KeyT, ValueT], KeyT]]:
    return st.tuples(st.just(map_), st.sampled_from(list(map_.keys())))


non_empty_maps_with_their_keys = non_empty_maps.flatmap(
    to_non_empty_maps_with_their_keys
)


def to_non_empty_maps_with_their_items(
    map_: Map[KeyT, ValueT], /
) -> st.SearchStrategy[tuple[Map[KeyT, ValueT], Item[KeyT, ValueT]]]:
    return st.tuples(st.just(map_), st.sampled_from(list(map_.items())))


non_empty_maps_with_their_items = non_empty_maps.flatmap(
    to_non_empty_maps_with_their_items
)


def is_key_external(map_with_key: tuple[Map[KeyT, ValueT], KeyT]) -> bool:
    map_, key = map_with_key
    return key not in map_


non_empty_maps_with_external_keys = non_empty_maps_with_keys.filter(
    is_key_external
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


def to_map_with_items_list(
    factory: Callable[..., Map[KeyT, ValueT]],
    items_lists_pair: tuple[
        list[Item[KeyT, ValueT]], list[Item[KeyT, ValueT]]
    ],
    /,
) -> tuple[Map[KeyT, ValueT], list[Item[KeyT, ValueT]]]:
    first_items_list, second_items_list = items_lists_pair
    return factory(*first_items_list), second_items_list


maps_with_items_lists = st.builds(
    to_map_with_items_list,
    factories,
    (
        value_with_order_strategy_strategy.flatmap(
            partial(
                to_value_sequences_with_order_strategy, sizes=[(0, None)] * 2
            )
        ).map(value_sequences_with_order_to_items_lists)
    ),
)


def to_maps_pair(
    factory: Callable[..., Map[KeyT, ValueT]],
    items_lists_pair: tuple[
        list[Item[KeyT, ValueT]], list[Item[KeyT, ValueT]]
    ],
    /,
) -> MapsPair[KeyT, ValueT]:
    first_items_list, second_items_list = items_lists_pair
    return factory(*first_items_list), factory(*second_items_list)


maps_pairs = st.builds(
    to_maps_pair,
    factories,
    value_with_order_strategy_strategy.flatmap(
        partial(to_value_sequences_with_order_strategy, sizes=[(0, None)] * 2)
    ).map(value_sequences_with_order_to_items_lists),
)
maps_with_items_lists_or_maps = maps_with_items_lists | maps_pairs
