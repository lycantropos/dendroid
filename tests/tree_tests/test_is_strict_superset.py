from typing import Tuple

from hypothesis import given

from dendroid.binary import Tree
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.trees)
def test_irreflexivity(tree: Tree) -> None:
    assert not tree > tree


@given(strategies.trees_pairs)
def test_asymmetry(trees_pair: Tuple[Tree, Tree]) -> None:
    first_tree, second_tree = trees_pair

    assert implication(first_tree > second_tree, not second_tree > first_tree)


@given(strategies.trees_triplets)
def test_transitivity(trees_triplet: Tuple[Tree, Tree, Tree]) -> None:
    first_tree, second_tree, third_tree = trees_triplet

    assert implication(first_tree > second_tree > third_tree,
                       first_tree > third_tree)


@given(strategies.trees_pairs)
def test_connection_with_lower_than(trees_pair: Tuple[Tree, Tree]) -> None:
    first_tree, second_tree = trees_pair

    assert equivalence(first_tree > second_tree, second_tree < first_tree)
