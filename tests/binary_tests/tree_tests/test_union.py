from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from . import strategies


@given(strategies.trees_pairs)
def test_basic(trees_pair: Tuple[Tree, Tree]) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert isinstance(result, Tree)
    assert len(result) <= len(left_tree) + len(right_tree)


@given(strategies.trees)
def test_idempotence(tree: Tree) -> None:
    result = tree | tree

    assert result == tree


@given(strategies.empty_trees, strategies.trees)
def test_left_neutral_element(empty_tree: Tree, tree: Tree) -> None:
    result = empty_tree | tree

    assert result == tree


@given(strategies.empty_trees, strategies.trees)
def test_right_neutral_element(empty_tree: Tree, tree: Tree) -> None:
    result = tree | empty_tree

    assert result == tree


@given(strategies.trees_pairs)
def test_absorption_identity(trees_pair: Tuple[Tree, Tree]) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | (left_tree & right_tree)

    assert result == left_tree


@given(strategies.trees_pairs)
def test_commutativity(trees_pair: Tuple[Tree, Tree]) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert result == right_tree | left_tree


@given(strategies.trees_triplets)
def test_associativity(trees_triplet: Tuple[Tree, Tree, Tree]) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree | mid_tree) | right_tree

    assert result == left_tree | (mid_tree | right_tree)


@given(strategies.trees_triplets)
def test_difference_operand(trees_triplet: Tuple[Tree, Tree, Tree]) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree - mid_tree) | right_tree

    assert result == (left_tree | right_tree) - (mid_tree - right_tree)


@given(strategies.trees_triplets)
def test_distribution_over_intersection(trees_triplet: Tuple[Tree, Tree, Tree]
                                        ) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree | (mid_tree & right_tree)

    assert result == (left_tree | mid_tree) & (left_tree | right_tree)


@given(strategies.trees_pairs)
def test_connection_with_subset_relation(trees_pair: Tuple[Tree, Tree]
                                         ) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert left_tree <= result and right_tree <= result
