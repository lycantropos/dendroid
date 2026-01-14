import copy

from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet

from . import strategies


@given(strategies.sets)
def test_shallow(set_: BaseSet[ValueT]) -> None:
    result = copy.copy(set_)

    assert result is not set_
    assert result == set_


@given(strategies.sets)
def test_deep(set_: BaseSet[ValueT]) -> None:
    result = copy.deepcopy(set_)

    assert result is not set_
    assert result == set_
