import pytest
from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    first,
    is_left_subtree_less_than_right_subtree,
    last,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.non_empty_sets_with_their_values)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    set_.remove(value)

    tree = set_.tree
    assert (
        to_min_binary_tree_height(tree)
        <= to_height(tree)
        <= to_max_binary_tree_height(tree)
    )
    assert value not in set_
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.remove(value)


@given(strategies.non_empty_sets)
def test_step_left(set_: BaseSet[ValueT]) -> None:
    value = first(set_)

    set_.remove(value)

    assert value not in set_


@given(strategies.non_empty_sets)
def test_step_right(set_: BaseSet[ValueT]) -> None:
    value = last(set_)

    set_.remove(value)

    assert value not in set_
