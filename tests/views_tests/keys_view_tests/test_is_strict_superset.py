from hypothesis import given

from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.keys_views)
def test_irreflexivity(keys_view: Set) -> None:
    assert not keys_view > keys_view


@given(strategies.keys_views_pairs)
def test_asymmetry(keys_views_pair: SetsPair) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert implication(first_keys_view > second_keys_view,
                       not second_keys_view > first_keys_view)


@given(strategies.keys_views_triplets)
def test_transitivity(keys_views_triplet: SetsTriplet) -> None:
    first_keys_view, second_keys_view, third_keys_view = keys_views_triplet

    assert implication(first_keys_view > second_keys_view > third_keys_view,
                       first_keys_view > third_keys_view)


@given(strategies.keys_views_pairs)
def test_connection_with_lower_than(keys_views_pair: SetsPair) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert equivalence(first_keys_view > second_keys_view,
                       second_keys_view < first_keys_view)
