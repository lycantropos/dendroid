from copy import deepcopy
from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from dendroid.hints import Domain
from . import strategies


@given(strategies.empty_trees, strategies.totally_ordered_values)
def test_basic(tree: Tree, value: Domain) -> None:
    result = tree.discard(value)

    assert result is None


@given(strategies.empty_trees, strategies.totally_ordered_values)
def test_base_case(tree: Tree, value: Domain) -> None:
    tree.discard(value)

    assert len(tree) == 0
    assert value not in tree


@given(strategies.non_empty_trees_with_totally_ordered_values)
def test_step(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value
    original = deepcopy(tree)

    tree.discard(value)

    assert len(tree) == len(original) - (value in original)
    assert value not in tree
