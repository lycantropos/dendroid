from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         are_keys_equal,
                         implication,
                         to_height,
                         to_max_binary_tree_height,
                         set_value_to_key)
from . import strategies


@given(strategies.non_empty_sets_with_values)
def test_properties(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    assert implication(value in set_,
                       are_keys_equal(set_value_to_key(set_, value),
                                      set_.tree.root.key))


@given(strategies.non_empty_sets)
def test_accessing_in_order(set_: Set) -> None:
    for value in set_:
        value in set_

    tree = set_.tree
    assert to_height(tree) == to_max_binary_tree_height(tree)
