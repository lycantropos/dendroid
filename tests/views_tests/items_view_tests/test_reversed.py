from hypothesis import given

from tests.utils import (ItemsView,
                         capacity,
                         pairwise)
from . import strategies


@given(strategies.items_views)
def test_size(items_view: ItemsView) -> None:
    result = reversed(items_view)

    assert capacity(result) == len(items_view)


@given(strategies.items_views)
def test_elements(items_view: ItemsView) -> None:
    result = reversed(items_view)

    assert all(element in items_view for element in result)


@given(strategies.items_views_with_two_or_more_values)
def test_order(items_view: ItemsView) -> None:
    result = reversed(items_view)

    assert all(next_item < item for item, next_item in pairwise(result))
