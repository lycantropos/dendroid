from hypothesis import given

from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.items_views)
def test_reflexivity(items_view: Set) -> None:
    assert items_view >= items_view


@given(strategies.items_views_pairs)
def test_antisymmetry(items_views_pair: SetsPair) -> None:
    first_tree, second_tree = items_views_pair

    assert equivalence(first_tree >= second_tree >= first_tree,
                       first_tree == second_tree)


@given(strategies.items_views_triplets)
def test_transitivity(items_views_triplet: SetsTriplet) -> None:
    first_tree, second_tree, third_tree = items_views_triplet

    assert implication(first_tree >= second_tree >= third_tree,
                       first_tree >= third_tree)


@given(strategies.items_views_pairs)
def test_connection_with_greater_than(items_views_pair: SetsPair) -> None:
    first_tree, second_tree = items_views_pair

    assert implication(first_tree > second_tree, first_tree >= second_tree)


@given(strategies.items_views_pairs)
def test_connection_with_lower_than_or_equals(
        items_views_pair: SetsPair) -> None:
    first_tree, second_tree = items_views_pair

    assert equivalence(first_tree >= second_tree, second_tree <= first_tree)
