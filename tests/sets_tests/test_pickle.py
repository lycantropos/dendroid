from hypothesis import given

from dendroid.sets import Set
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sets)
def test_round_trip(set_: Set) -> None:
    assert pickle_round_trip(set_) == set_
