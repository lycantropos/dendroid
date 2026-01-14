from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map, pickle_round_trip

from . import strategies


@given(strategies.maps)
def test_round_trip(map_: Map[KeyT, ValueT]) -> None:
    assert pickle_round_trip(map_) == map_
