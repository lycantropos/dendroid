from hypothesis import given

from tests.utils import (Tree,
                         TreesPair,
                         TreesTriplet,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.trees_pairs)
def test_basic(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree & right_tree

    assert isinstance(result, type(left_tree))


@given(strategies.trees_pairs)
def test_properties(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree & right_tree

    assert len(result) <= min(len(left_tree), len(right_tree))
    assert (to_min_binary_tree_height(result)
            <= to_height(result)
            <= min(to_height(left_tree), to_height(right_tree),
                   to_max_binary_tree_height(result)))
    assert all(value in left_tree and value in right_tree
               for value in result)
    assert (not result
            or not result.isdisjoint(left_tree)
            and not result.isdisjoint(right_tree))
    assert is_left_subtree_less_than_right_subtree(result)


@given(strategies.trees)
def test_idempotence(tree: Tree) -> None:
    result = tree & tree

    assert result == tree


@given(strategies.empty_trees_with_trees)
def test_left_absorbing_element(empty_tree_with_tree: TreesPair) -> None:
    empty_tree, tree = empty_tree_with_tree

    result = empty_tree & tree

    assert len(result) == 0
    assert not result


@given(strategies.empty_trees_with_trees)
def test_right_absorbing_element(empty_tree_with_tree: TreesPair) -> None:
    empty_tree, tree = empty_tree_with_tree

    result = tree & empty_tree

    assert len(result) == 0
    assert not result


@given(strategies.trees_pairs)
def test_absorption_identity(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree & (left_tree | right_tree)

    assert result == left_tree


@given(strategies.trees_pairs)
def test_commutativity(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree & right_tree

    assert result == right_tree & left_tree


@given(strategies.trees_triplets)
def test_associativity(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree & mid_tree) & right_tree

    assert result == left_tree & (mid_tree & right_tree)


@given(strategies.trees_triplets)
def test_difference_operand(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree - mid_tree) & right_tree

    assert result == (left_tree & right_tree) - mid_tree


@given(strategies.trees_triplets)
def test_distribution_over_union(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree & (mid_tree | right_tree)

    assert result == (left_tree & mid_tree) | (left_tree & right_tree)


@given(strategies.trees_pairs)
def test_connection_with_subset_relation(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree & right_tree

    assert result <= left_tree and result <= right_tree
