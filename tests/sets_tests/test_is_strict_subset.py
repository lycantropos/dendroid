from hypothesis import given

from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.sets)
def test_irreflexivity(set_: Set) -> None:
    assert not set_ < set_


@given(strategies.sets_pairs)
def test_asymmetry(sets_pair: SetsPair) -> None:
    first_set, second_set = sets_pair

    assert implication(first_set < second_set, not second_set < first_set)


@given(strategies.sets_triplets)
def test_transitivity(sets_triplet: SetsTriplet) -> None:
    first_set, second_set, third_set = sets_triplet

    assert implication(first_set < second_set < third_set,
                       first_set < third_set)


@given(strategies.sets_pairs)
def test_connection_with_greater_than(sets_pair: SetsPair) -> None:
    first_set, second_set = sets_pair

    assert equivalence(first_set < second_set, second_set > first_set)
