from copy import copy
from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         SetsPair,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.sets_pairs)
def test_basic(sets_pair: SetsPair) -> None:
    first_tree, second_tree = sets_pair

    result = first_tree.isdisjoint(second_tree)

    assert isinstance(result, bool)


@given(strategies.empty_sets_with_sets)
def test_base_case(empty_tree_with_tree: SetsPair) -> None:
    empty_tree, set_ = empty_tree_with_tree

    assert empty_tree.isdisjoint(set_)


@given(strategies.sets_pairs_with_values)
def test_step(two_sets_with_value: Tuple[Set, Set, Value]) -> None:
    left_set, right_set, value = two_sets_with_value
    original = copy(left_set)

    left_set.add(value)

    assert implication(not original.isdisjoint(right_set),
                       not left_set.isdisjoint(right_set))
    assert implication(original.isdisjoint(right_set),
                       equivalence(left_set.isdisjoint(right_set),
                                   value not in right_set))


@given(strategies.sets_pairs)
def test_symmetry(sets_pair: SetsPair) -> None:
    first_tree, second_tree = sets_pair

    assert equivalence(first_tree.isdisjoint(second_tree),
                       second_tree.isdisjoint(first_tree))
