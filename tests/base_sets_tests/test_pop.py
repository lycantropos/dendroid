from copy import copy

import pytest
from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    is_left_subtree_less_than_right_subtree,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.non_empty_sets)
def test_properties(set_: BaseSet[ValueT]) -> None:
    result = set_.pop()

    tree = set_._tree
    assert (
        to_min_binary_tree_height(tree)
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert result not in set_
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_sets)
def test_base_case(set_: BaseSet[ValueT]) -> None:
    with pytest.raises(ValueError):
        set_.pop()


@given(strategies.non_empty_sets)
def test_step(set_: BaseSet[ValueT]) -> None:
    original = copy(set_)

    result = set_.pop()

    assert result in original
    assert result not in set_
    assert len(set_) == len(original) - 1
