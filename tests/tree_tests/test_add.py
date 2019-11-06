from copy import deepcopy
from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.trees_with_values)
def test_basic(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    result = tree.add(value)

    assert result is None


@given(strategies.trees_with_values)
def test_properties(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.add(value)

    assert len(tree) > 0
    assert to_height(tree) > 0
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_trees_with_values)
def test_base_case(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.add(value)

    assert len(tree) == 1
    assert value in tree


@given(strategies.trees_with_values)
def test_step(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value
    original = deepcopy(tree)

    tree.add(value)

    assert len(tree) == len(original) + (value not in original)
    assert value in tree
