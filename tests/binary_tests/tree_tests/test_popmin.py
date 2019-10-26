import pytest
from hypothesis import given

from dendroid.binary import Tree
from . import strategies


@given(strategies.empty_trees)
def test_base_case(tree: Tree) -> None:
    with pytest.raises(KeyError):
        tree.popmin()


@given(strategies.non_empty_trees)
def test_step(tree: Tree) -> None:
    result = tree.popmin()

    assert result not in tree
    assert all(result < value
               if tree.key is None
               else tree.key(result) < tree.key(value)
               for value in tree)
