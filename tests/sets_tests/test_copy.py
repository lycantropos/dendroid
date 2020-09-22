import copy

from hypothesis import given

from tests.utils import Set
from . import strategies


@given(strategies.sets)
def test_shallow(set_: Set) -> None:
    result = copy.copy(set_)

    assert result is not set_
    assert result == set_


@given(strategies.sets)
def test_deep(set_: Set) -> None:
    result = copy.deepcopy(set_)

    assert result is not set_
    assert result == set_
