import pytest
from hypothesis import given

from dendroid.utils import to_balanced_tree_height
from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: Tree) -> None:
    result = tree.popmax()

    assert to_height(tree) >= to_balanced_tree_height(len(tree))
    assert result not in tree
    assert all(result > value
               if tree.key is None
               else tree.key(result) > tree.key(value)
               for value in tree)
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_trees)
def test_base_case(tree: Tree) -> None:
    with pytest.raises(KeyError):
        tree.popmax()


@given(strategies.non_empty_trees)
def test_step(tree: Tree) -> None:
    result = tree.popmax()

    assert result not in tree
    assert all(result > value
               if tree.key is None
               else tree.key(result) > tree.key(value)
               for value in tree)
