from typing import Tuple

from hypothesis import given

from dendroid.hints import Item
from tests.utils import (ItemsView,
                         are_items_equal,
                         are_items_keys_equal,
                         equivalence,
                         to_items_view_including_item)
from . import strategies


@given(strategies.empty_items_views_with_items)
def test_base_case(items_view_with_item: Tuple[ItemsView, Item]) -> None:
    items_view, item = items_view_with_item

    assert item not in items_view


@given(strategies.items_views_with_items_pairs)
def test_step(
        items_view_with_items_pair: Tuple[ItemsView, Tuple[Item, Item]]
) -> None:
    items_view, (extra_item, item) = items_view_with_items_pair

    next_items_view = to_items_view_including_item(items_view, extra_item)

    assert equivalence(item in next_items_view,
                       (item in items_view
                        and not are_items_keys_equal(item, extra_item))
                       or are_items_equal(item, extra_item))
