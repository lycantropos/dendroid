from copy import copy

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


@given(strategies.sets_with_values)
def test_type(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    result = set_.add(value)

    assert result is None


@given(strategies.sets_with_values)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    set_.add(value)

    tree = set_._tree
    assert len(set_) > 0
    assert set_
    assert (
        max(0, to_min_binary_tree_height(tree))
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    set_.add(value)

    assert len(set_) == 1
    assert set_
    assert value in set_


@given(strategies.sets_with_values)
def test_step(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value
    original = copy(set_)

    set_.add(value)

    assert len(set_) == len(original) + (value not in original)
    assert value in set_
