from hypothesis import given

from tests.hints import KeyT
from tests.utils import (
    KeysView,
    KeysViewsPair,
    KeysViewsTriplet,
    equivalence,
    implication,
)

from . import strategies


@given(strategies.keys_views)
def test_reflexivity(keys_view: KeysView[KeyT]) -> None:
    assert keys_view >= keys_view


@given(strategies.keys_views_pairs)
def test_antisymmetry(keys_views_pair: KeysViewsPair[KeyT]) -> None:
    first_tree, second_tree = keys_views_pair

    assert equivalence(
        first_tree >= second_tree >= first_tree, first_tree == second_tree
    )


@given(strategies.keys_views_triplets)
def test_transitivity(keys_views_triplet: KeysViewsTriplet[KeyT]) -> None:
    first_tree, second_tree, third_tree = keys_views_triplet

    assert implication(
        first_tree >= second_tree >= third_tree, first_tree >= third_tree
    )


@given(strategies.keys_views_pairs)
def test_connection_with_greater_than(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    first_tree, second_tree = keys_views_pair

    assert implication(first_tree > second_tree, first_tree >= second_tree)


@given(strategies.keys_views_pairs)
def test_connection_with_lower_than_or_equals(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    first_tree, second_tree = keys_views_pair

    assert equivalence(first_tree >= second_tree, second_tree <= first_tree)
