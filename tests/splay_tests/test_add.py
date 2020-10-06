from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (BaseSet,
                         are_keys_equal,
                         set_value_to_key)
from . import strategies


@given(strategies.sets_with_values)
def test_properties(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    set_.add(value)

    assert are_keys_equal(set_value_to_key(set_, value), set_.tree.root.key)
