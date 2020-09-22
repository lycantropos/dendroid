from hypothesis import given

from tests.utils import (Set,
                         are_keys_equal,
                         value_to_key)
from . import strategies


@given(strategies.non_empty_sets)
def test_properties(set_: Set) -> None:
    result = set_.max()

    assert are_keys_equal(value_to_key(set_, result), set_.tree.root.key)
    assert result is set_.tree.root.value
