from hypothesis import given

from tests.utils import (Set,
                         SetsPair,
                         SetsTriplet,
                         equivalence,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.sets_pairs)
def test_basic(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set | right_set

    assert isinstance(result, type(left_set))


@given(strategies.sets_pairs)
def test_properties(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set | right_set

    result_tree = result.tree
    assert len(result) <= len(left_set) + len(right_set)
    assert (to_min_binary_tree_height(result_tree)
            <= to_height(result_tree)
            <= min(to_height(left_set.tree) + to_height(right_set.tree) + 1,
                   to_max_binary_tree_height(result_tree)))
    assert (all(value in result
                for value in left_set)
            and all(value in result
                    for value in right_set))
    assert ((not left_set or not result.isdisjoint(left_set))
            and (not right_set or not result.isdisjoint(right_set)))
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.sets)
def test_idempotence(set_: Set) -> None:
    result = set_ | set_

    assert result == set_


@given(strategies.empty_sets_with_sets)
def test_left_neutral_element(empty_tree_with_tree: SetsPair) -> None:
    empty_tree, set_ = empty_tree_with_tree

    result = empty_tree | set_

    assert result == set_


@given(strategies.empty_sets_with_sets)
def test_right_neutral_element(empty_tree_with_tree: SetsPair) -> None:
    empty_tree, set_ = empty_tree_with_tree

    result = set_ | empty_tree

    assert result == set_


@given(strategies.sets_pairs)
def test_absorption_identity(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set | (left_set & right_set)

    assert result == left_set


@given(strategies.sets_pairs)
def test_commutativity(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set | right_set

    assert result == right_set | left_set


@given(strategies.sets_triplets)
def test_associativity(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = (left_set | mid_tree) | right_set

    assert result == left_set | (mid_tree | right_set)


@given(strategies.sets_triplets)
def test_difference_operand(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = (left_set - mid_tree) | right_set

    assert result == (left_set | right_set) - (mid_tree - right_set)


@given(strategies.sets_triplets)
def test_distribution_over_intersection(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = left_set | (mid_tree & right_set)

    assert result == (left_set | mid_tree) & (left_set | right_set)


@given(strategies.sets_pairs)
def test_connection_with_subset_relation(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set | right_set

    assert left_set <= result and right_set <= result


@given(strategies.sets_pairs)
def test_connection_with_disjoint(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set | right_set

    assert equivalence(left_set.isdisjoint(right_set),
                       len(result) == len(left_set) + len(right_set))
