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
def test_type(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set - right_set

    assert isinstance(result, type(left_set))


@given(strategies.sets_pairs)
def test_properties(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set - right_set

    result_tree = result.tree
    assert len(result) <= len(left_set)
    assert (to_min_binary_tree_height(result_tree)
            <= to_height(result_tree)
            <= to_max_binary_tree_height(result_tree))
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.sets)
def test_self_inverse(set_: Set) -> None:
    result = set_ - set_

    assert len(result) == 0


@given(strategies.empty_sets_with_sets)
def test_left_absorbing_element(empty_tree_with_tree: SetsPair) -> None:
    empty_tree, set_ = empty_tree_with_tree

    result = empty_tree - set_

    assert len(result) == 0


@given(strategies.empty_sets_with_sets)
def test_right_neutral_element(empty_tree_with_tree: SetsPair) -> None:
    empty_tree, set_ = empty_tree_with_tree

    result = set_ - empty_tree

    assert result == set_


@given(strategies.sets_pairs)
def test_expressing_intersection_as_difference(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set - (left_set - right_set)

    assert result == left_set & right_set


@given(strategies.sets_triplets)
def test_difference_subtrahend(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = left_set - (mid_tree - right_set)

    assert result == (left_set - mid_tree) | (left_set & right_set)


@given(strategies.sets_triplets)
def test_intersection_minuend(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = (left_set & mid_tree) - right_set

    assert result == left_set & (mid_tree - right_set)


@given(strategies.sets_triplets)
def test_intersection_subtrahend(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = left_set - (mid_tree & right_set)

    assert result == (left_set - mid_tree) | (left_set - right_set)


@given(strategies.sets_triplets)
def test_union_subtrahend(sets_triplet: SetsTriplet) -> None:
    left_set, mid_tree, right_set = sets_triplet

    result = left_set - (mid_tree | right_set)

    assert result == (left_set - mid_tree) & (left_set - right_set)


@given(strategies.sets_pairs)
def test_connection_with_subset_relation(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set - right_set

    assert result <= left_set


@given(strategies.sets_pairs)
def test_connection_with_disjoint(sets_pair: SetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set - right_set

    assert equivalence(left_set.isdisjoint(right_set), result == left_set)
