from copy import deepcopy

import pytest
from hypothesis import given

from dendroid.binary import Tree
from . import strategies


@given(strategies.empty_trees)
def test_base_case(tree: Tree) -> None:
    with pytest.raises(KeyError):
        tree.pop()


@given(strategies.non_empty_trees)
def test_step(tree: Tree) -> None:
    original = deepcopy(tree)

    result = tree.pop()

    assert result in original
    assert result not in tree
    assert len(tree) == len(original) - 1
