from collections.abc import Callable, Sequence
from functools import partial
from itertools import starmap
from typing import Any

from hypothesis import strategies

from dendroid import avl, binary, red_black, splay
from dendroid.hints import Item
from tests.hints import KeyT, ValueT
from tests.strategies import (
    single_values_with_orders,
    to_values_lists_with_orders,
    two_or_more_values_with_orders,
    values_lists_with_orders,
    values_with_orders_strategies,
)
from tests.utils import (
    Map,
    ValueSequenceWithOrder,
    ValueSequencesWithOrder,
    ValuesView,
    compose,
    has_size_two_or_more,
)

factories = strategies.sampled_from(
    [binary.map_, avl.map_, red_black.map_, splay.map_]
).map(partial(compose, Map.values))


def values_list_with_order_to_items_list(
    values_list_with_order: ValueSequenceWithOrder[ValueT, KeyT], /
) -> Sequence[Item[Any, ValueT]]:
    values_list, order = values_list_with_order
    return (
        [(value, value) for value in values_list]
        if order is None
        else [(order(value), value) for value in values_list]
    )


items_lists = values_lists_with_orders.map(
    values_list_with_order_to_items_list
)
single_items = single_values_with_orders.map(
    values_list_with_order_to_items_list
)
two_or_more_items = two_or_more_values_with_orders.map(
    values_list_with_order_to_items_list
)


def to_values_view(
    factory: Callable[..., ValuesView[ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> ValuesView[ValueT]:
    return factory(*items)


values_views = strategies.builds(to_values_view, factories, items_lists)
values_views_with_two_or_more_values = strategies.builds(
    to_values_view, factories, two_or_more_items
).filter(has_size_two_or_more)


def to_values_view_with_value(
    factory: Callable[..., ValuesView[ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> tuple[ValuesView[ValueT], ValueT]:
    *rest_items, (_, value) = items
    return factory(*rest_items), value


empty_values_views_with_values = strategies.builds(
    to_values_view_with_value, factories, single_items
)


def values_lists_with_order_to_items_lists(
    values_lists_with_order: ValueSequencesWithOrder[ValueT, KeyT], /
) -> tuple[list[Item[KeyT, ValueT]] | list[tuple[ValueT, ValueT]], ...]:
    values_lists, order = values_lists_with_order
    return (
        tuple(
            [(value, value) for value in values_list]
            for values_list in values_lists
        )
        if order is None
        else tuple(
            [(order(value), value) for value in values_list]
            for values_list in values_lists
        )
    )


def to_values_views_tuple(
    factory: Callable[..., ValuesView[ValueT]],
    items_lists: list[list[Item[KeyT, ValueT]]],
) -> tuple[ValuesView[ValueT], ...]:
    return tuple(starmap(factory, items_lists))


values_views_pairs = strategies.builds(
    to_values_views_tuple,
    factories,
    (
        values_with_orders_strategies.flatmap(
            partial(to_values_lists_with_orders, sizes=[(0, None)] * 2)
        ).map(values_lists_with_order_to_items_lists)
    ),
)
values_views_triplets = strategies.builds(
    to_values_views_tuple,
    factories,
    (
        values_with_orders_strategies.flatmap(
            partial(to_values_lists_with_orders, sizes=[(0, None)] * 3)
        ).map(values_lists_with_order_to_items_lists)
    ),
)
