import pytest
from hypothesis import given

from tests.utils import Tree
from . import strategies


@given(strategies.empty_trees)
def test_basic(tree: Tree) -> None:
    iterator = iter(tree)

    with pytest.raises(StopIteration):
        next(iterator)


@given(strategies.non_empty_trees)
def test_step(tree: Tree) -> None:
    iterator = iter(tree)

    result = next(iterator)

    assert result in tree
    assert result == tree.min()
