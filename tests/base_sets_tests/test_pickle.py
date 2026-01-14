from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, pickle_round_trip

from . import strategies


@given(strategies.sets)
def test_round_trip(set_: BaseSet[ValueT]) -> None:
    assert pickle_round_trip(set_) == set_
