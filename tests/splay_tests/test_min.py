from hypothesis import given

from tests.hints import ValueT
from tests.utils import BaseSet, NIL, are_keys_equal, set_value_to_key

from . import strategies


@given(strategies.non_empty_sets)
def test_properties(set_: BaseSet[ValueT]) -> None:
    result = set_.min()

    root_node = set_._tree.root
    assert root_node is not NIL
    assert are_keys_equal(set_value_to_key(set_, result), root_node.key)
    assert result is root_node.value
