import math
import sys

from hypothesis import given

from tests.hints import ValueT
from tests.utils import ValuesView

from . import strategies


@given(strategies.values_views)
def test_evaluation(values_view: ValuesView[ValueT]) -> None:
    result = repr(values_view)

    type_ = type(values_view)
    # `math` module is required for `inf` object
    assert (
        repr(
            eval(
                result,
                {**sys.modules},
                {**vars(math), type_.__qualname__: type_},
            )
        )
        == result
    )
