from hypothesis import given
from lz.iterating import (capacity,
                          pairwise)

from tests.utils import ItemsView
from . import strategies


@given(strategies.items_views)
def test_size(items_view: ItemsView) -> None:
    result = reversed(items_view)

    assert capacity(result) == len(items_view)


@given(strategies.items_views)
def test_elements(items_view: ItemsView) -> None:
    result = reversed(items_view)

    assert all(value in items_view for value in result)


@given(strategies.items_views_with_two_or_more_values)
def test_order(items_view: ItemsView) -> None:
    result = reversed(items_view)

    assert all(next_item < item for item, next_item in pairwise(result))
