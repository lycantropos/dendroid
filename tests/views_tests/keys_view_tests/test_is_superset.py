from hypothesis import given

from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.keys_views)
def test_reflexivity(keys_view: Set) -> None:
    assert keys_view >= keys_view


@given(strategies.keys_views_pairs)
def test_antisymmetry(keys_views_pair: SetsPair) -> None:
    first_tree, second_tree = keys_views_pair

    assert equivalence(first_tree >= second_tree >= first_tree,
                       first_tree == second_tree)


@given(strategies.keys_views_triplets)
def test_transitivity(keys_views_triplet: SetsTriplet) -> None:
    first_tree, second_tree, third_tree = keys_views_triplet

    assert implication(first_tree >= second_tree >= third_tree,
                       first_tree >= third_tree)


@given(strategies.keys_views_pairs)
def test_connection_with_greater_than(keys_views_pair: SetsPair) -> None:
    first_tree, second_tree = keys_views_pair

    assert implication(first_tree > second_tree, first_tree >= second_tree)


@given(strategies.keys_views_pairs)
def test_connection_with_lower_than_or_equals(keys_views_pair: SetsPair) -> None:
    first_tree, second_tree = keys_views_pair

    assert equivalence(first_tree >= second_tree, second_tree <= first_tree)
