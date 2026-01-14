from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    ValuesView,
    ValuesViewsPair,
    ValuesViewsTriplet,
    equivalence,
    implication,
)

from . import strategies


@given(strategies.values_views)
def test_reflexivity(values_view: ValuesView[ValueT]) -> None:
    assert values_view == values_view


@given(strategies.values_views_pairs)
def test_symmetry(values_views_pair: ValuesViewsPair[ValueT]) -> None:
    first_values_view, second_values_view = values_views_pair

    assert equivalence(
        first_values_view == second_values_view,
        second_values_view == first_values_view,
    )


@given(strategies.values_views_triplets)
def test_transitivity(
    values_views_triplet: ValuesViewsTriplet[ValueT],
) -> None:
    first_values_view, second_values_view, third_values_view = (
        values_views_triplet
    )

    assert implication(
        first_values_view == second_values_view
        and second_values_view == third_values_view,
        first_values_view == third_values_view,
    )


@given(strategies.values_views_pairs)
def test_connection_with_inequality(
    values_views_pair: ValuesViewsPair[ValueT],
) -> None:
    first_values_view, second_values_view = values_views_pair

    assert equivalence(
        first_values_view != second_values_view,
        first_values_view != second_values_view,
    )
