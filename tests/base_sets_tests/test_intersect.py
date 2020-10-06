from hypothesis import given

from tests.utils import (BaseSet,
                         BaseSetsPair,
                         BaseSetsTriplet,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.sets_pairs)
def test_type(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set & right_set

    assert isinstance(result, type(left_set))


@given(strategies.sets_pairs)
def test_properties(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set & right_set

    result_tree = result.tree
    assert len(result) <= min(len(left_set), len(right_set))
    assert (to_min_binary_tree_height(result_tree)
            <= to_height(result_tree)
            <= min(to_height(left_set.tree), to_height(right_set.tree),
                   to_max_binary_tree_height(result_tree)))
    assert all(value in left_set and value in right_set for value in result)
    assert (not result
            or not result.isdisjoint(left_set)
            and not result.isdisjoint(right_set))
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.sets)
def test_idempotence(set_: BaseSet) -> None:
    result = set_ & set_

    assert result == set_


@given(strategies.empty_sets_with_sets)
def test_left_absorbing_element(empty_set_with_set: BaseSetsPair) -> None:
    empty_set, set_ = empty_set_with_set

    result = empty_set & set_

    assert len(result) == 0
    assert not result


@given(strategies.empty_sets_with_sets)
def test_right_absorbing_element(empty_set_with_set: BaseSetsPair) -> None:
    empty_set, set_ = empty_set_with_set

    result = set_ & empty_set

    assert len(result) == 0
    assert not result


@given(strategies.sets_pairs)
def test_absorption_identity(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set & (left_set | right_set)

    assert result == left_set


@given(strategies.sets_pairs)
def test_commutativity(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set & right_set

    assert result == right_set & left_set


@given(strategies.sets_triplets)
def test_associativity(sets_triplet: BaseSetsTriplet) -> None:
    left_set, mid_set, right_set = sets_triplet

    result = (left_set & mid_set) & right_set

    assert result == left_set & (mid_set & right_set)


@given(strategies.sets_triplets)
def test_difference_operand(sets_triplet: BaseSetsTriplet) -> None:
    left_set, mid_set, right_set = sets_triplet

    result = (left_set - mid_set) & right_set

    assert result == (left_set & right_set) - mid_set


@given(strategies.sets_triplets)
def test_distribution_over_union(sets_triplet: BaseSetsTriplet) -> None:
    left_set, mid_set, right_set = sets_triplet

    result = left_set & (mid_set | right_set)

    assert result == (left_set & mid_set) | (left_set & right_set)


@given(strategies.sets_pairs)
def test_connection_with_subset_relation(sets_pair: BaseSetsPair) -> None:
    left_set, right_set = sets_pair

    result = left_set & right_set

    assert result <= left_set and result <= right_set
