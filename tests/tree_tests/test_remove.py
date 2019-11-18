from typing import Tuple

import pytest
from hypothesis import given
from lz.iterating import (first,
                          last)

from dendroid.hints import Domain
from dendroid.utils import to_balanced_tree_height
from tests.utils import (Tree,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.non_empty_trees_with_their_values)
def test_properties(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    tree.remove(value)

    assert to_height(tree) >= to_balanced_tree_height(len(tree))
    assert value not in tree
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_trees_with_values)
def test_base_case(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

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
