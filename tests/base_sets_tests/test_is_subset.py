from hypothesis import given

from tests.utils import (BaseSet,
                         BaseSetsPair,
                         BaseSetsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.sets)
def test_reflexivity(set_: BaseSet) -> None:
    assert set_ <= set_


@given(strategies.sets_pairs)
def test_antisymmetry(sets_pair: BaseSetsPair) -> None:
    first_set, second_set = sets_pair

    assert equivalence(first_set <= second_set <= first_set,
                       first_set == second_set)


@given(strategies.sets_triplets)
def test_transitivity(sets_triplet: BaseSetsTriplet) -> None:
    first_set, second_set, third_set = sets_triplet

    assert implication(first_set <= second_set <= third_set,
                       first_set <= third_set)


@given(strategies.sets_pairs)
def test_connection_with_lower_than(sets_pair: BaseSetsPair) -> None:
    first_set, second_set = sets_pair

    assert implication(first_set < second_set, first_set <= second_set)


@given(strategies.sets_pairs)
def test_connection_with_greater_than_or_equals(sets_pair: BaseSetsPair
                                                ) -> None:
    first_set, second_set = sets_pair

    assert equivalence(first_set <= second_set, second_set >= first_set)
