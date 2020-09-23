from hypothesis import given
from lz.iterating import (capacity)

from tests.utils import ValuesView
from . import strategies


@given(strategies.values_views)
def test_size(values_view: ValuesView) -> None:
    result = iter(values_view)

    assert capacity(result) == len(values_view)


@given(strategies.values_views)
def test_elements(values_view: ValuesView) -> None:
    result = iter(values_view)

    assert all(element in values_view
               for element in result)
