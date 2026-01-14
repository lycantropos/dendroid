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
    assert keys_view <= keys_view


@given(strategies.keys_views_pairs)
def test_antisymmetry(keys_views_pair: KeysViewsPair[KeyT]) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert equivalence(
        first_keys_view <= second_keys_view <= first_keys_view,
        first_keys_view == second_keys_view,
    )


@given(strategies.keys_views_triplets)
def test_transitivity(keys_views_triplet: KeysViewsTriplet[KeyT]) -> None:
    first_keys_view, second_keys_view, third_keys_view = keys_views_triplet

    assert implication(
        first_keys_view <= second_keys_view <= third_keys_view,
        first_keys_view <= third_keys_view,
    )


@given(strategies.keys_views_pairs)
def test_connection_with_lower_than(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert implication(
        first_keys_view < second_keys_view, first_keys_view <= second_keys_view
    )


@given(strategies.keys_views_pairs)
def test_connection_with_greater_than_or_equals(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert equivalence(
        first_keys_view <= second_keys_view,
        second_keys_view >= first_keys_view,
    )
