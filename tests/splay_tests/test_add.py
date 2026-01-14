from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, NIL, are_keys_equal, set_value_to_key

from . import strategies


@given(strategies.sets_with_values)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    set_.add(value)

    assert (root_node := set_.tree.root) is not NIL
    assert are_keys_equal(set_value_to_key(set_, value), root_node.key)
