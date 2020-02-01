from hypothesis import given

from tests.utils import (Tree,
                         TreesPair,
                         TreesTriplet,
                         equivalence,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.trees_pairs)
def test_basic(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - right_tree

    assert isinstance(result, type(left_tree))


@given(strategies.trees_pairs)
def test_properties(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - right_tree

    assert len(result) <= len(left_tree)
    assert (to_min_binary_tree_height(result)
            <= to_height(result)
            <= to_max_binary_tree_height(result))
    assert is_left_subtree_less_than_right_subtree(result)


@given(strategies.trees)
def test_self_inverse(tree: Tree) -> None:
    result = tree - tree

    assert len(result) == 0
    assert not result


@given(strategies.empty_trees_with_trees)
def test_left_absorbing_element(empty_tree_with_tree: TreesPair) -> None:
    empty_tree, tree = empty_tree_with_tree

    result = empty_tree - tree

    assert len(result) == 0
    assert not result


@given(strategies.empty_trees_with_trees)
def test_right_neutral_element(empty_tree_with_tree: TreesPair) -> None:
    empty_tree, tree = empty_tree_with_tree

    result = tree - empty_tree

    assert result == tree


@given(strategies.trees_pairs)
def test_expressing_intersection_as_difference(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - (left_tree - right_tree)

    assert result == left_tree & right_tree


@given(strategies.trees_triplets)
def test_difference_subtrahend(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree - (mid_tree - right_tree)

    assert result == (left_tree - mid_tree) | (left_tree & right_tree)


@given(strategies.trees_triplets)
def test_intersection_minuend(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree & mid_tree) - right_tree

    assert result == left_tree & (mid_tree - right_tree)


@given(strategies.trees_triplets)
def test_intersection_subtrahend(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree - (mid_tree & right_tree)

    assert result == (left_tree - mid_tree) | (left_tree - right_tree)


@given(strategies.trees_triplets)
def test_union_subtrahend(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree - (mid_tree | right_tree)

    assert result == (left_tree - mid_tree) & (left_tree - right_tree)


@given(strategies.trees_pairs)
def test_connection_with_subset_relation(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - right_tree

    assert result <= left_tree


@given(strategies.trees_pairs)
def test_connection_with_disjoint(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - right_tree

    assert equivalence(left_tree.isdisjoint(right_tree), result == left_tree)
