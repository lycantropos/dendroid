from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (Set,
                         are_keys_equal,
                         value_to_key)
from . import strategies


@given(strategies.non_empty_sets_with_their_non_max_values)
def test_properties(set_with_value: Tuple[Set, Value]) -> None:
    set_, value = set_with_value

    result = set_.next(value)

    assert are_keys_equal(value_to_key(set_, result), set_.tree.root.key)
    assert result is set_.tree.root.value
