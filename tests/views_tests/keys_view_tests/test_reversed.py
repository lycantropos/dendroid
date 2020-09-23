from hypothesis import given
from lz.iterating import (capacity,
                          pairwise)

from tests.utils import KeysView
from . import strategies


@given(strategies.keys_views)
def test_size(keys_view: KeysView) -> None:
    result = reversed(keys_view)

    assert capacity(result) == len(keys_view)


@given(strategies.keys_views)
def test_elements(keys_view: KeysView) -> None:
    result = reversed(keys_view)

    assert all(value in keys_view for value in result)


@given(strategies.keys_views_with_two_or_more_values)
def test_order(keys_view: KeysView) -> None:
    result = reversed(keys_view)

    assert all(next_key < key for key, next_key in pairwise(result))
