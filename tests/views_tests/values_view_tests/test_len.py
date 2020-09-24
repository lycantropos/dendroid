from hypothesis import given

from tests.utils import (ValuesView,
                         equivalence)
from . import strategies


@given(strategies.values_views)
def test_properties(values_view_: ValuesView) -> None:
    result = len(values_view_)

    assert result >= 0
    assert equivalence(bool(result), bool(values_view_))
