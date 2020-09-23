from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         SetsPair,
                         equivalence,
                         implication,
                         to_set_including_value)
from . import strategies


@given(strategies.sets_pairs)
def test_type(sets_pair: SetsPair) -> None:
    first_set, second_set = sets_pair

    result = first_set.isdisjoint(second_set)

    assert isinstance(result, bool)


@given(strategies.empty_sets_with_sets)
def test_base_case(empty_set_with_set: SetsPair) -> None:
    empty_set, set_ = empty_set_with_set

    assert empty_set.isdisjoint(set_)


@given(strategies.sets_pairs_with_values)
def test_step(two_sets_with_value: Tuple[Set, Set, Value]) -> None:
    left_set, right_set, value = two_sets_with_value

    next_left_set = to_set_including_value(left_set, value)

    assert implication(not left_set.isdisjoint(right_set),
                       not next_left_set.isdisjoint(right_set))
    assert implication(left_set.isdisjoint(right_set),
                       equivalence(next_left_set.isdisjoint(right_set),
                                   value not in right_set))


@given(strategies.sets_pairs)
def test_symmetry(sets_pair: SetsPair) -> None:
    first_set, second_set = sets_pair

    assert equivalence(first_set.isdisjoint(second_set),
                       second_set.isdisjoint(first_set))
