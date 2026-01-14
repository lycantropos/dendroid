from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import ItemsView, equivalence

from . import strategies


@given(strategies.items_views)
def test_properties(items_view_: ItemsView[KeyT, ValueT]) -> None:
    result = len(items_view_)

    assert result >= 0
    assert equivalence(bool(result), bool(items_view_))
