from collections.abc import Callable, Sequence
from functools import partial
from itertools import starmap
from operator import attrgetter
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
    Node,
    Tree,
    ValueSequenceWithOrder,
    ValueSequencesWithOrder,
    compose,
    has_size_two_or_more,
)

factories = st.sampled_from(
    [binary.map_, avl.map_, red_black.map_, splay.map_]
).map(partial(compose, attrgetter('tree')))


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
non_empty_items_lists = non_empty_value_sequence_with_order_strategy.map(
    values_list_with_order_to_items_list
)
single_items = single_value_with_order_strategy.map(
    values_list_with_order_to_items_list
)
two_or_more_items = two_or_more_values_with_order_strategy.map(
    values_list_with_order_to_items_list
)


def to_tree(
    factory: Callable[..., Tree[KeyT, ValueT]],
    items: list[Item[KeyT, ValueT]],
    /,
) -> Tree[KeyT, ValueT]:
    return factory(*items)


empty_trees = st.builds(to_tree, factories, st.builds(list))
trees = st.builds(to_tree, factories, items_lists)
non_empty_trees = st.builds(to_tree, factories, non_empty_items_lists)
trees_with_two_or_more_nodes = st.builds(
    to_tree, factories, two_or_more_items
).filter(has_size_two_or_more)


def to_tree_with_key(
    factory: Callable[..., Tree[KeyT, ValueT]], items: list[Item[KeyT, ValueT]]
) -> tuple[Tree[KeyT, ValueT], KeyT]:
    *rest_items, (key, _) = items
    return factory(*rest_items), key


empty_trees_with_keys = st.builds(to_tree_with_key, factories, single_items)
trees_with_keys = st.builds(to_tree_with_key, factories, non_empty_items_lists)


def to_non_empty_trees_with_their_keys(
    tree: Tree[KeyT, ValueT], /
) -> st.SearchStrategy[tuple[Tree[KeyT, ValueT], KeyT]]:
    return st.tuples(st.just(tree), st.sampled_from(tree.keys))


non_empty_trees_with_their_keys = non_empty_trees.flatmap(
    to_non_empty_trees_with_their_keys
)


def to_non_empty_trees_with_their_nodes(
    tree: Tree[KeyT, ValueT], /
) -> st.SearchStrategy[tuple[Tree[KeyT, ValueT], Node[KeyT, ValueT]]]:
    return st.tuples(st.just(tree), st.sampled_from(list(tree)))


non_empty_trees_with_their_nodes = non_empty_trees.flatmap(
    to_non_empty_trees_with_their_nodes
)


def value_sequences_with_order_to_items_lists(
    value_sequences_with_order: ValueSequencesWithOrder[ValueT, KeyT], /
) -> tuple[list[Item[KeyT, ValueT]] | list[tuple[ValueT, ValueT]], ...]:
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


def to_trees_tuple(
    factory: Callable[..., Tree[KeyT, ValueT]],
    items_lists: list[list[Item[KeyT, ValueT]]],
    /,
) -> tuple[Tree[KeyT, ValueT], ...]:
    return tuple(starmap(factory, items_lists))


trees_pairs = st.builds(
    to_trees_tuple,
    factories,
    (
        value_with_order_strategy_strategy.flatmap(
            partial(
                to_value_sequences_with_order_strategy, sizes=[(0, None)] * 2
            )
        ).map(value_sequences_with_order_to_items_lists)
    ),
)
trees_triplets = st.builds(
    to_trees_tuple,
    factories,
    (
        value_with_order_strategy_strategy.flatmap(
            partial(
                to_value_sequences_with_order_strategy, sizes=[(0, None)] * 3
            )
        ).map(value_sequences_with_order_to_items_lists)
    ),
)
