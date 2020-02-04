import math
import sys

from hypothesis import given

from tests.utils import Tree
from . import strategies


@given(strategies.trees)
def test_basic(tree: Tree) -> None:
    result = repr(tree)

    type_ = type(tree)

    assert result.startswith(type_.__module__)
    assert type_.__qualname__ in result


@given(strategies.trees_with_none_keys)
def test_evaluation(tree: Tree) -> None:
    result = repr(tree)

    # `math` module is required for `inf` object
    assert eval(result, sys.modules, vars(math)) == tree
