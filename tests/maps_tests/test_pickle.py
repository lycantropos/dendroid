from hypothesis import given

from tests.utils import (Map,
                         pickle_round_trip)
from . import strategies


@given(strategies.maps)
def test_round_trip(map_: Map) -> None:
    assert pickle_round_trip(map_) == map_
