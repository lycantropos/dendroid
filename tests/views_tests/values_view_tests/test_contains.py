from hypothesis import given

from tests.hints import ValueT
from tests.utils import ValuesView

from . import strategies


@given(strategies.empty_values_views_with_values)
def test_base_case(
    values_view_with_value: tuple[ValuesView[ValueT], ValueT],
) -> None:
    values_view, value = values_view_with_value

    assert value not in values_view
