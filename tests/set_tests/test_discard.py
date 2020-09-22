from copy import copy
from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.sets_with_values)
def test_basic(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    result = set_.discard(value)

    assert result is None


@given(strategies.sets_with_values)
def test_properties(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    set_.discard(value)

    tree = set_.tree
    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    set_.discard(value)

    assert len(set_) == 0
    assert not set_
    assert value not in set_


@given(strategies.non_empty_sets_with_values)
def test_step(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value
    original = copy(set_)

    set_.discard(value)

    assert len(set_) == len(original) - (value in original)
    assert value not in set_
