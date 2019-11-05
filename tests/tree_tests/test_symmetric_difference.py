from hypothesis import given

from tests.utils import (Tree,
                         TreesPair,
                         TreesTriplet)
from . import strategies


@given(strategies.trees_pairs)
def test_basic(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = left_tree ^ right_tree

    assert isinstance(result, type(left_tree))
    assert len(result) <= len(left_tree) + len(right_tree)


@given(strategies.trees)
def test_self_inverse(tree: Tree) -> None:
    result = tree ^ tree

    assert len(result) == 0


@given(strategies.empty_trees, strategies.trees)
def test_left_neutral_element(empty_tree: Tree, tree: Tree) -> None:
    result = empty_tree ^ tree

    assert result == tree


@given(strategies.empty_trees, strategies.trees)
def test_right_neutral_element(empty_tree: Tree, tree: Tree) -> None:
    result = tree ^ empty_tree

    assert result == tree


@given(strategies.trees_pairs)
def test_equivalent_using_union_of_differences(trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = (left_tree - right_tree) | (right_tree - left_tree)

    assert result == left_tree ^ right_tree


@given(strategies.trees_pairs)
def test_equivalent_using_difference_of_union_and_intersection(
        trees_pair: TreesPair) -> None:
    left_tree, right_tree = trees_pair

    result = (left_tree | right_tree) - (right_tree & left_tree)

    assert result == left_tree ^ right_tree


@given(strategies.trees_pairs)
def test_expressing_union_as_symmetric_difference(trees_pair: TreesPair
                                                  ) -> None:
    left_tree, right_tree = trees_pair

    result = (left_tree ^ right_tree) ^ (left_tree & right_tree)

    assert result == left_tree | right_tree


@given(strategies.trees_triplets)
def test_repeated(trees_triplet: TreesTriplet) -> None:
    left_tree, mid_tree, right_tree = trees_triplet

    result = (left_tree ^ mid_tree) ^ (mid_tree ^ right_tree)

    assert result == left_tree ^ right_tree
