from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import ItemsView, capacity, pairwise

from . import strategies


@given(strategies.items_views)
def test_size(items_view: ItemsView[KeyT, ValueT]) -> None:
    result = iter(items_view)

    assert capacity(result) == len(items_view)


@given(strategies.items_views)
def test_elements(items_view: ItemsView[KeyT, ValueT]) -> None:
    result = iter(items_view)

    assert all(element in items_view for element in result)


@given(strategies.items_views_with_two_or_more_values)
def test_order(items_view: ItemsView[KeyT, ValueT]) -> None:
    result = iter(items_view)

    assert all(item < next_item for item, next_item in pairwise(result))
