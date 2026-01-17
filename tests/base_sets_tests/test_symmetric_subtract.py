from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    BaseSetsPair,
    BaseSetsTriplet,
    equivalence,
    is_left_subtree_less_than_right_subtree,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.sets_pairs)
def test_type(sets_pair: BaseSetsPair[ValueT]) -> None:
    left_set, right_set = sets_pair

    result = left_set ^ right_set

    assert isinstance(result, type(left_set))


@given(strategies.sets_pairs)
def test_properties(sets_pair: BaseSetsPair[ValueT]) -> None:
    left_set, right_set = sets_pair

    result = left_set ^ right_set

    result_tree = result._tree
    assert len(result) <= len(left_set) + len(right_set)
    assert (
        to_min_binary_tree_height(result_tree)
        <= to_height(result_tree)
        <= min(
            to_height(left_set._tree) + to_height(right_set._tree) + 1,
            to_max_binary_tree_height(result_tree),
        )
    )
    assert all(
        (value in left_set) is not (value in right_set) for value in result
    )
    assert left_set <= right_set or not result.isdisjoint(left_set)
    assert right_set <= left_set or not result.isdisjoint(right_set)
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.sets)
def test_self_inverse(set_: BaseSet[ValueT]) -> None:
    result = set_ ^ set_

    assert len(result) == 0


@given(strategies.empty_sets_with_sets)
def test_left_neutral_element(
    empty_set_with_set: BaseSetsPair[ValueT],
) -> None:
    empty_set, set_ = empty_set_with_set

    result = empty_set ^ set_

    assert result == set_


@given(strategies.empty_sets_with_sets)
def test_right_neutral_element(
    empty_set_with_set: BaseSetsPair[ValueT],
) -> None:
    empty_set, set_ = empty_set_with_set

    result = set_ ^ empty_set

    assert result == set_


@given(strategies.sets_pairs)
def test_commutativity(sets_pair: BaseSetsPair[ValueT]) -> None:
    left_set, right_set = sets_pair

    result = left_set ^ right_set

    assert result == right_set ^ left_set


@given(strategies.sets_triplets)
def test_associativity(sets_triplet: BaseSetsTriplet[ValueT]) -> None:
    left_set, mid_set, right_set = sets_triplet

    result = (left_set ^ mid_set) ^ right_set

    assert result == left_set ^ (mid_set ^ right_set)


@given(strategies.sets_pairs)
def test_equivalent_using_union_of_differences(
    sets_pair: BaseSetsPair[ValueT],
) -> None:
    left_set, right_set = sets_pair

    result = (left_set - right_set) | (right_set - left_set)

    assert result == left_set ^ right_set


@given(strategies.sets_pairs)
def test_equivalent_using_difference_of_union_and_intersection(
    sets_pair: BaseSetsPair[ValueT],
) -> None:
    left_set, right_set = sets_pair

    result = (left_set | right_set) - (right_set & left_set)

    assert result == left_set ^ right_set


@given(strategies.sets_pairs)
def test_expressing_union_as_symmetric_difference(
    sets_pair: BaseSetsPair[ValueT],
) -> None:
    left_set, right_set = sets_pair

    result = (left_set ^ right_set) ^ (left_set & right_set)

    assert result == left_set | right_set


@given(strategies.sets_triplets)
def test_repeated(sets_triplet: BaseSetsTriplet[ValueT]) -> None:
    left_set, mid_set, right_set = sets_triplet

    result = (left_set ^ mid_set) ^ (mid_set ^ right_set)

    assert result == left_set ^ right_set


@given(strategies.sets_pairs)
def test_connection_with_disjoint(sets_pair: BaseSetsPair[ValueT]) -> None:
    left_set, right_set = sets_pair

    result = left_set ^ right_set

    assert equivalence(
        left_set.isdisjoint(right_set), result == left_set | right_set
    )
