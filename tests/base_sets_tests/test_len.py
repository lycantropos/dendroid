from hypothesis import given

from tests.utils import (BaseSet,
                         equivalence)
from . import strategies


@given(strategies.sets)
def test_properties(set_: BaseSet) -> None:
    result = len(set_)

    assert result >= 0
    assert equivalence(bool(result), bool(set_))
