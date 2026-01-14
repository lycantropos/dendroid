from collections.abc import Callable, Sequence
from functools import partial
from itertools import starmap
from typing import Any

from hypothesis import strategies

from dendroid import avl, binary, red_black, splay
from dendroid.hints import Item
from tests.hints import KeyT, ValueT
from tests.strategies import (
    non_empty_values_lists_with_orders,
    single_values_with_orders,
    to_values_lists_with_orders,
    two_or_more_values_with_orders,
    values_lists_with_orders,
    values_with_orders_strategies,
)
from tests.utils import (
    ItemsView,
    Map,
    ValueSequenceWithOrder,
    ValueSequencesWithOrder,
    compose,
    has_size_two_or_more,
)

factories = strategies.sampled_from(
    [binary.map_, avl.map_, red_black.map_, splay.map_]
).map(partial(compose, Map.items))


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
non_empty_items_lists = non_empty_values_lists_with_orders.map(
    values_list_with_order_to_items_list
)
single_items = single_values_with_orders.map(
    values_list_with_order_to_items_list
)
two_or_more_items = two_or_more_values_with_orders.map(
    values_list_with_order_to_items_list
)


def to_items_view(
    factory: Callable[..., ItemsView[KeyT, ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> ItemsView[KeyT, ValueT]:
    return factory(*items)


empty_items_views = strategies.builds(
    to_items_view, factories, strategies.builds(list)
)
items_views = strategies.builds(to_items_view, factories, items_lists)
empty_items_views_with_items_views = strategies.tuples(
    empty_items_views, items_views
)
non_empty_items_views = strategies.builds(
    to_items_view, factories, non_empty_items_lists
)
items_views_with_two_or_more_values = strategies.builds(
    to_items_view, factories, two_or_more_items
).filter(has_size_two_or_more)


def to_items_view_with_item(
    factory: Callable[..., ItemsView[KeyT, ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> tuple[ItemsView[KeyT, ValueT], Item[KeyT, ValueT]]:
    *rest_items, item = items
    return factory(*rest_items), item


empty_items_views_with_items = strategies.builds(
    to_items_view_with_item, factories, single_items
)


def to_items_view_with_items_pair(
    factory: Callable[..., ItemsView[KeyT, ValueT]],
    items_list: list[Item[KeyT, ValueT]],
    /,
) -> tuple[
    ItemsView[KeyT, ValueT], tuple[Item[KeyT, ValueT], Item[KeyT, ValueT]]
]:
    *rest_items, first_item, second_item = items_list
    return factory(*rest_items), (first_item, second_item)


items_views_with_items_pairs = strategies.builds(
    to_items_view_with_items_pair, factories, two_or_more_items
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


def to_items_views_tuple(
    factory: Callable[..., ItemsView[KeyT, ValueT]],
    items_lists: list[list[Item[KeyT, ValueT]]],
    /,
) -> tuple[ItemsView[KeyT, ValueT], ...]:
    return tuple(starmap(factory, items_lists))


items_views_pairs = strategies.builds(
    to_items_views_tuple,
    factories,
    (
        values_with_orders_strategies.flatmap(
            partial(to_values_lists_with_orders, sizes=[(0, None)] * 2)
        ).map(values_lists_with_order_to_items_lists)
    ),
)
items_views_triplets = strategies.builds(
    to_items_views_tuple,
    factories,
    (
        values_with_orders_strategies.flatmap(
            partial(to_values_lists_with_orders, sizes=[(0, None)] * 3)
        ).map(values_lists_with_order_to_items_lists)
    ),
)


def to_items_views_pair_with_item(
    factory: Callable[..., ItemsView[KeyT, ValueT]],
    items_lists_pair: tuple[
        list[Item[KeyT, ValueT]], list[Item[KeyT, ValueT]]
    ],
    /,
) -> tuple[
    ItemsView[KeyT, ValueT], ItemsView[KeyT, ValueT], Item[KeyT, ValueT]
]:
    (*first_items, item), second_items = items_lists_pair
    return factory(*first_items), factory(*second_items), item


items_views_pairs_with_items = strategies.builds(
    to_items_views_pair_with_item,
    factories,
    values_with_orders_strategies.flatmap(
        partial(to_values_lists_with_orders, sizes=[(1, None), (0, None)])
    ).map(values_lists_with_order_to_items_lists),
)
