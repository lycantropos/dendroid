from copy import deepcopy

import pytest
from hypothesis import given

from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree)
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: Tree) -> None:
    result = tree.pop()

    assert result not in tree
    assert is_left_subtree_less_than_right_subtree(result)


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
