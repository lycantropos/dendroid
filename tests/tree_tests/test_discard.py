from copy import deepcopy
from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.trees_with_values)
def test_basic(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    result = tree.discard(value)

    assert result is None


@given(strategies.trees_with_values)
def test_properties(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.discard(value)

    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert value not in tree
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_trees_with_values)
def test_base_case(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.discard(value)

    assert len(tree) == 0
    assert value not in tree


@given(strategies.non_empty_trees_with_values)
def test_step(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value
    original = deepcopy(tree)

    tree.discard(value)

    assert len(tree) == len(original) - (value in original)
    assert value not in tree
