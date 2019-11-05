from hypothesis import given

from tests.utils import (Tree,
                         TreesPair,
                         TreesTriplet,
                         implication,
                         is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.trees_pairs)
def test_basic(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert isinstance(result, type(left_tree))


@given(strategies.trees_pairs)
def test_properties(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert len(result) <= len(left_tree) + len(right_tree)
    assert to_height(result) <= to_height(left_tree) + to_height(right_tree)
    assert (all(value in result
                for value in left_tree)
            and all(value in result
                    for value in right_tree))
    assert ((not left_tree or not result.isdisjoint(left_tree))
            and (not right_tree or not result.isdisjoint(right_tree)))
    assert is_left_subtree_less_than_right_subtree(result)


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
def test_absorption_identity(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | (left_tree & right_tree)

    assert result == left_tree


@given(strategies.trees_pairs)
def test_commutativity(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert result == right_tree | left_tree


@given(strategies.trees_triplets)
def test_associativity(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree | mid_tree) | right_tree

    assert result == left_tree | (mid_tree | right_tree)


@given(strategies.trees_triplets)
def test_difference_operand(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree - mid_tree) | right_tree

    assert result == (left_tree | right_tree) - (mid_tree - right_tree)


@given(strategies.trees_triplets)
def test_distribution_over_intersection(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree | (mid_tree & right_tree)

    assert result == (left_tree | mid_tree) & (left_tree | right_tree)


@given(strategies.trees_pairs)
def test_connection_with_subset_relation(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert left_tree <= result and right_tree <= result


@given(strategies.trees_pairs)
def test_connection_with_disjoint(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree | right_tree

    assert implication(left_tree.isdisjoint(right_tree),
                       len(result) == len(left_tree) + len(right_tree))
