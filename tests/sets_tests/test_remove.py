from typing import Tuple

import pytest
from hypothesis import given
from lz.iterating import (first,
                          last)

from dendroid.hints import Value
from tests.utils import (Set,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.non_empty_sets_with_their_values)
def test_properties(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    set_.remove(value)

    tree = set_.tree
    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert value not in set_
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    with pytest.raises(ValueError):
        set_.remove(value)


@given(strategies.non_empty_sets)
def test_step_left(set_: Set) -> None:
    value = first(set_)

    set_.remove(value)

    assert value not in set_


@given(strategies.non_empty_sets)
def test_step_right(set_: Set) -> None:
    value = last(set_)

    set_.remove(value)

    assert value not in set_
