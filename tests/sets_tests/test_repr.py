import math
import sys

from hypothesis import given

from tests.utils import Set
from . import strategies


@given(strategies.sets)
def test_basic(set_: Set) -> None:
    result = repr(set_)

    type_ = type(set_)

    assert result.startswith(type_.__qualname__)


@given(strategies.sets_with_none_orders)
def test_evaluation(set_: Set) -> None:
    result = repr(set_)

    type_ = type(set_)
    # `math` module is required for `inf` object
    assert eval(result, sys.modules,
                {**vars(math), type_.__qualname__: type_}) == set_
