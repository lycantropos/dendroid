from copy import deepcopy

import pytest
from hypothesis import given

from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: Tree) -> None:
    result = tree.pop()

    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert result not in tree
    assert is_left_subtree_less_than_right_subtree(tree)


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
