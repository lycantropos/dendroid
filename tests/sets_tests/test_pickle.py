from hypothesis import given

from tests.utils import (Set,
                         pickle_round_trip)
from . import strategies


@given(strategies.sets)
def test_round_trip(set_: Set) -> None:
    assert pickle_round_trip(set_) == set_
