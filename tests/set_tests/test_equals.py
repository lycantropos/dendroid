from hypothesis import given

from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.sets)
def test_reflexivity(set_: Set) -> None:
    assert set_ == set_


@given(strategies.sets_pairs)
def test_symmetry(sets_pair: SetsPair) -> None:
    first_tree, second_tree = sets_pair

    assert equivalence(first_tree == second_tree,
                       second_tree == first_tree)


@given(strategies.sets_triplets)
def test_transitivity(sets_triplet: SetsTriplet) -> None:
    first_tree, second_tree, third_tree = sets_triplet

    assert implication(first_tree == second_tree and second_tree == third_tree,
                       first_tree == third_tree)


@given(strategies.sets_pairs)
def test_connection_with_inequality(sets_pair: SetsPair) -> None:
    first_tree, second_tree = sets_pair

    assert equivalence(not first_tree == second_tree,
                       first_tree != second_tree)
