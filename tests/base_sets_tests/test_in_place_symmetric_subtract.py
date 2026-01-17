from copy import copy

from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSetsPair,
    is_left_subtree_less_than_right_subtree,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.sets_pairs)
def test_connection_with_symmetric_difference(
    sets_pair: BaseSetsPair[ValueT],
) -> None:
    left_set, right_set = sets_pair
    original_left_set = copy(left_set)

    left_set ^= right_set

    assert left_set == original_left_set ^ right_set


@given(strategies.sets_pairs)
def test_properties(sets_pair: BaseSetsPair[ValueT]) -> None:
    left_set, right_set = sets_pair

    left_set ^= right_set

    left_tree = left_set._tree
    assert (
        to_min_binary_tree_height(left_tree)
        <= to_height(left_tree)
        <= to_max_binary_tree_height(left_tree)
    )
    assert is_left_subtree_less_than_right_subtree(left_tree)
