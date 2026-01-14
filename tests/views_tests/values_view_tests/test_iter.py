from hypothesis import given

from tests.hints import ValueT
from tests.utils import ValuesView, capacity

from . import strategies


@given(strategies.values_views)
def test_size(values_view: ValuesView[ValueT]) -> None:
    result = iter(values_view)

    assert capacity(result) == len(values_view)


@given(strategies.values_views)
def test_elements(values_view: ValuesView[ValueT]) -> None:
    result = iter(values_view)

    assert all(element in values_view for element in result)
