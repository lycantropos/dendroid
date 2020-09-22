from hypothesis import given

from dendroid.utils import are_keys_equal
from tests.utils import (Set,
                         value_to_key)
from . import strategies


@given(strategies.non_empty_sets)
def test_properties(set_: Set) -> None:
    result = set_.max()

    assert are_keys_equal(value_to_key(set_, result), set_.tree.root.key)
    assert result is set_.tree.root.value
