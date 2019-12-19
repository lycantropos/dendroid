import copy

from hypothesis import given

from tests.utils import Tree
from . import strategies


@given(strategies.trees)
def test_shallow(tree: Tree) -> None:
    result = copy.copy(tree)

    assert result is not tree
    assert result == tree


@given(strategies.trees)
def test_deep(tree: Tree) -> None:
    result = copy.deepcopy(tree)

    assert result is not tree
    assert result == tree
