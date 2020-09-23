from hypothesis import given
from lz.iterating import (capacity)

from tests.utils import ValuesView
from . import strategies


@given(strategies.values_views)
def test_size(values_view: ValuesView) -> None:
    result = reversed(values_view)

    assert capacity(result) == len(values_view)


@given(strategies.values_views)
def test_elements(values_view: ValuesView) -> None:
    result = reversed(values_view)

    assert all(value in values_view for value in result)
