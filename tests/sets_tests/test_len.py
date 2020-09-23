from hypothesis import given

from tests.utils import (Set,
                         equivalence)
from . import strategies


@given(strategies.sets)
def test_properties(set_: Set) -> None:
    result = len(set_)

    assert result >= 0
    assert equivalence(bool(result), bool(set_))
