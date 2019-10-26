from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from . import strategies


@given(strategies.trees)
def test_self_inverse(tree: Tree) -> None:
    result = tree - tree

    assert len(result) == 0


@given(strategies.empty_trees, strategies.trees)
def test_left_absorbing_element(empty_tree: Tree, tree: Tree) -> None:
    result = empty_tree - tree

    assert len(result) == 0


@given(strategies.empty_trees, strategies.trees)
def test_right_neutral_element(empty_tree: Tree, tree: Tree) -> None:
    result = tree - empty_tree

    assert result == tree


@given(strategies.trees_pairs)
def test_expressing_intersection_as_difference(trees_pair: Tuple[Tree, Tree]
                                               ) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - (left_tree - right_tree)

    assert result == left_tree & right_tree


@given(strategies.trees_triplets)
def test_difference_subtrahend(trees_triplet: Tuple[Tree, Tree, Tree]) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree - (mid_tree - right_tree)

    assert result == (left_tree - mid_tree) | (left_tree & right_tree)


@given(strategies.trees_triplets)
def test_intersection_minuend(trees_triplet: Tuple[Tree, Tree, Tree]) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree & mid_tree) - right_tree

    assert result == left_tree & (mid_tree - right_tree)


@given(strategies.trees_triplets)
def test_intersection_subtrahend(trees_triplet: Tuple[Tree, Tree, Tree]
                                 ) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree - (mid_tree & right_tree)

    assert result == (left_tree - mid_tree) | (left_tree - right_tree)


@given(strategies.trees_triplets)
def test_union_subtrahend(trees_triplet: Tuple[Tree, Tree, Tree]) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = left_tree - (mid_tree | right_tree)

    assert result == (left_tree - mid_tree) & (left_tree - right_tree)


@given(strategies.trees_pairs)
def test_connection_with_subset_relation(trees_pair: Tuple[Tree, Tree]
                                         ) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree - right_tree

    assert result <= left_tree
