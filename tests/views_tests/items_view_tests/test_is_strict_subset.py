from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import (
    ItemsView,
    ItemsViewsPair,
    ItemsViewsTriplet,
    equivalence,
    implication,
)

from . import strategies


@given(strategies.items_views)
def test_irreflexivity(items_view: ItemsView[KeyT, ValueT]) -> None:
    assert not items_view < items_view


@given(strategies.items_views_pairs)
def test_asymmetry(items_views_pair: ItemsViewsPair[KeyT, ValueT]) -> None:
    first_items_view, second_items_view = items_views_pair

    assert implication(
        first_items_view < second_items_view,
        not second_items_view < first_items_view,
    )


@given(strategies.items_views_triplets)
def test_transitivity(
    items_views_triplet: ItemsViewsTriplet[KeyT, ValueT],
) -> None:
    first_items_view, second_items_view, third_items_view = items_views_triplet

    assert implication(
        first_items_view < second_items_view < third_items_view,
        first_items_view < third_items_view,
    )


@given(strategies.items_views_pairs)
def test_connection_with_greater_than(
    items_views_pair: ItemsViewsPair[KeyT, ValueT],
) -> None:
    first_items_view, second_items_view = items_views_pair

    assert equivalence(
        first_items_view < second_items_view,
        second_items_view > first_items_view,
    )
