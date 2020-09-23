import math
import sys

from hypothesis import given

from tests.utils import Tree
from . import strategies


@given(strategies.trees)
def test_evaluation(tree: Tree) -> None:
    result = repr(tree)

    # `math` module is required for `inf` object
    assert repr(eval(result, sys.modules, vars(math))) == result
