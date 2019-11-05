import pytest
from hypothesis import given
from lz.iterating import (first,
                          last)

from dendroid.hints import Domain
from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree)
from . import strategies


@given(strategies.non_empty_trees_with_values_from_them)
def test_properties(tree_with_value: Tree) -> None:
    tree, value = tree_with_value

    tree.remove(value)

    assert value not in tree
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_trees, strategies.totally_ordered_values)
def test_base_case(tree: Tree, value: Domain) -> None:
    with pytest.raises(KeyError):
        tree.remove(value)


@given(strategies.non_empty_trees)
def test_step_left(tree: Tree) -> None:
    value = first(tree)

    tree.remove(value)

    assert value not in tree


@given(strategies.non_empty_trees)
def test_step_right(tree: Tree) -> None:
    value = last(tree)

    tree.remove(value)

    assert value not in tree
