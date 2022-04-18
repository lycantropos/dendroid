from typing import Tuple

from hypothesis import given

from dendroid.hints import Item
from tests.utils import (ItemsView,
                         ItemsViewsPair,
                         equivalence,
                         implication,
                         to_items_view_including_item)
from . import strategies


@given(strategies.items_views_pairs)
def test_type(items_views_pair: ItemsViewsPair) -> None:
    first_items_view, second_items_view = items_views_pair

    result = first_items_view.isdisjoint(second_items_view)

    assert isinstance(result, bool)


@given(strategies.empty_items_views_with_items_views)
def test_base_case(empty_items_view_with_items_view: ItemsViewsPair) -> None:
    empty_items_view, items_view = empty_items_view_with_items_view

    assert empty_items_view.isdisjoint(items_view)


@given(strategies.items_views_pairs_with_items)
def test_step(two_items_views_with_value: Tuple[ItemsView, ItemsView, Item]
              ) -> None:
    left_items_view, right_items_view, item = two_items_views_with_value

    next_left_items_view = to_items_view_including_item(left_items_view, item)

    assert implication(not left_items_view.isdisjoint(right_items_view),
                       not next_left_items_view.isdisjoint(right_items_view)
                       or (len(left_items_view) == 1
                           and item not in left_items_view))
    assert implication(left_items_view.isdisjoint(right_items_view),
                       equivalence(next_left_items_view
                                   .isdisjoint(right_items_view),
                                   item not in right_items_view))


@given(strategies.items_views_pairs)
def test_symmetry(items_views_pair: ItemsViewsPair) -> None:
    first_items_view, second_items_view = items_views_pair

    assert equivalence(first_items_view.isdisjoint(second_items_view),
                       second_items_view.isdisjoint(first_items_view))
