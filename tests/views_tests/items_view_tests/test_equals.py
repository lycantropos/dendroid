from hypothesis import given

from tests.utils import (ItemsView,
                         ItemsViewsPair,
                         ItemsViewsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.items_views)
def test_reflexivity(items_view: ItemsView) -> None:
    assert items_view == items_view


@given(strategies.items_views_pairs)
def test_symmetry(items_views_pair: ItemsViewsPair) -> None:
    first_items_view, second_items_view = items_views_pair

    assert equivalence(first_items_view == second_items_view,
                       second_items_view == first_items_view)


@given(strategies.items_views_triplets)
def test_transitivity(items_views_triplet: ItemsViewsTriplet) -> None:
    first_items_view, second_items_view, third_items_view = items_views_triplet

    assert implication(first_items_view == second_items_view
                       and second_items_view == third_items_view,
                       first_items_view == third_items_view)


@given(strategies.items_views_pairs)
def test_connection_with_inequality(items_views_pair: ItemsViewsPair) -> None:
    first_items_view, second_items_view = items_views_pair

    assert equivalence(not first_items_view == second_items_view,
                       first_items_view != second_items_view)
