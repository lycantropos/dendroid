from hypothesis import given

from tests.utils import (KeysView,
                         equivalence)
from . import strategies


@given(strategies.keys_views)
def test_properties(keys_view_: KeysView) -> None:
    result = len(keys_view_)

    assert result >= 0
    assert equivalence(bool(result), bool(keys_view_))
