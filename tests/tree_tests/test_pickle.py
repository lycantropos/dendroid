from hypothesis import given

from tests.utils import (Tree,
                         pickle_round_trip)
from . import strategies


@given(strategies.trees)
def test_round_trip(tree: Tree) -> None:
    assert pickle_round_trip(tree) == tree
