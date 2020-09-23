from hypothesis import given

from tests.utils import (KeysView,
                         KeysViewsPair,
                         KeysViewsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.keys_views)
def test_reflexivity(keys_view: KeysView) -> None:
    assert keys_view == keys_view


@given(strategies.keys_views_pairs)
def test_symmetry(keys_views_pair: KeysViewsPair) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert equivalence(first_keys_view == second_keys_view,
                       second_keys_view == first_keys_view)


@given(strategies.keys_views_triplets)
def test_transitivity(keys_views_triplet: KeysViewsTriplet) -> None:
    first_keys_view, second_keys_view, third_keys_view = keys_views_triplet

    assert implication(first_keys_view == second_keys_view
                       and second_keys_view == third_keys_view,
                       first_keys_view == third_keys_view)


@given(strategies.keys_views_pairs)
def test_connection_with_inequality(keys_views_pair: KeysViewsPair) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert equivalence(not first_keys_view == second_keys_view,
                       first_keys_view != second_keys_view)
