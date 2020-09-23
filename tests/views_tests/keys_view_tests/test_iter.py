from hypothesis import given
from lz.iterating import (capacity,
                          pairwise)

from tests.utils import KeysView
from . import strategies


@given(strategies.keys_views)
def test_size(keys_view: KeysView) -> None:
    result = iter(keys_view)

    assert capacity(result) == len(keys_view)


@given(strategies.keys_views)
def test_elements(keys_view: KeysView) -> None:
    result = iter(keys_view)

    assert all(element in keys_view for element in result)


@given(strategies.keys_views_with_two_or_more_values)
def test_order(keys_view: KeysView) -> None:
    result = iter(keys_view)

    assert all(key < next_key for key, next_key in pairwise(result))
