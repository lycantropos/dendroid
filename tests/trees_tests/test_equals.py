from hypothesis import given

from tests.utils import (Tree,
                         TreesPair,
                         TreesTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.trees)
def test_reflexivity(tree: Tree) -> None:
    assert tree == tree


@given(strategies.trees_pairs)
def test_symmetry(trees_pair: TreesPair) -> None:
    first_tree, second_tree = trees_pair

    assert equivalence(first_tree == second_tree, second_tree == first_tree)


@given(strategies.trees_triplets)
def test_transitivity(trees_triplet: TreesTriplet) -> None:
    first_tree, second_tree, third_tree = trees_triplet

    assert implication(first_tree == second_tree and second_tree == third_tree,
                       first_tree == third_tree)


@given(strategies.trees_pairs)
def test_connection_with_inequality(trees_pair: TreesPair) -> None:
    first_tree, second_tree = trees_pair

    assert equivalence(not first_tree == second_tree,
                       first_tree != second_tree)
