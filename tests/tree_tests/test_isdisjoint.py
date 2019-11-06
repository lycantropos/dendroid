from copy import deepcopy
from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import (Tree,
                         TreesPair,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.trees_pairs)
def test_basic(trees_pair: TreesPair) -> None:
    first_tree, second_tree = trees_pair

    result = first_tree.isdisjoint(second_tree)

    assert isinstance(result, bool)


@given(strategies.empty_trees_with_trees)
def test_base_case(empty_tree_with_tree: TreesPair) -> None:
    empty_tree, tree = empty_tree_with_tree

    assert empty_tree.isdisjoint(tree)


@given(strategies.trees_pairs_with_values)
def test_step(two_trees_with_value: Tuple[Tree, Tree, Domain]) -> None:
    left_tree, right_tree, value = two_trees_with_value
    original = deepcopy(left_tree)

    left_tree.add(value)

    assert implication(not original.isdisjoint(right_tree),
                       not left_tree.isdisjoint(right_tree))
    assert implication(original.isdisjoint(right_tree),
                       equivalence(left_tree.isdisjoint(right_tree),
                                   value not in right_tree))


@given(strategies.trees_pairs)
def test_symmetry(trees_pair: TreesPair) -> None:
    first_tree, second_tree = trees_pair

    assert equivalence(first_tree.isdisjoint(second_tree),
                       second_tree.isdisjoint(first_tree))
