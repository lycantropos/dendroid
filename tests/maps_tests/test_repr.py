import math
import sys

from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map

from . import strategies


@given(strategies.maps)
def test_evaluation(map_: Map[KeyT, ValueT]) -> None:
    result = repr(map_)

    type_ = type(map_)
    # `math` module is required for `inf` object
    assert (
        eval(
            result, {**sys.modules}, {**vars(math), type_.__qualname__: type_}
        )
        == map_
    )
