from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, NIL, are_keys_equal, set_value_to_key

from . import strategies


@given(strategies.non_empty_sets_with_their_non_min_values)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    result = set_.prev(value)

    root_node = set_.tree.root
    assert root_node is not NIL
    assert are_keys_equal(set_value_to_key(set_, result), root_node.key)
    assert result is root_node.value
