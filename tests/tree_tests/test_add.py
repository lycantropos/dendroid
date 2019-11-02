from copy import deepcopy
from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from dendroid.hints import Domain
from . import strategies


@given(strategies.trees_with_totally_ordered_values)
def test_basic(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    result = tree.add(value)

    assert result is None


@given(strategies.empty_trees, strategies.totally_ordered_values)
def test_base_case(tree: Tree, value: Domain) -> None:
    tree.add(value)

    assert len(tree) == 1
    assert value in tree


@given(strategies.trees_with_totally_ordered_values)
def test_step(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value
    original = deepcopy(tree)

    tree.add(value)

    assert len(tree) == len(original) + (value not in original)
    assert value in tree
