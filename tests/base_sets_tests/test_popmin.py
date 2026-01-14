import pytest
from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    is_left_subtree_less_than_right_subtree,
    set_value_to_key,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.non_empty_sets)
def test_properties(set_: BaseSet[ValueT]) -> None:
    set_.popmin()

    tree = set_.tree
    assert (
        to_min_binary_tree_height(tree)
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_sets)
def test_base_case(set_: BaseSet[ValueT]) -> None:
    with pytest.raises(ValueError):
        set_.popmin()


@given(strategies.non_empty_sets)
def test_step(set_: BaseSet[ValueT]) -> None:
    result = set_.popmin()

    assert result not in set_
    assert all(
        set_value_to_key(set_, result) < set_value_to_key(set_, value)
        for value in set_
    )
