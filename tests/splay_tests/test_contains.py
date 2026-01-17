from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    NIL,
    are_keys_equal,
    implication,
    set_value_to_key,
    to_height,
    to_max_binary_tree_height,
)

from . import strategies


@given(strategies.non_empty_sets_with_values)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    assert implication(
        value in set_,
        (
            (root_node := set_._tree.root) is not NIL
            and are_keys_equal(set_value_to_key(set_, value), root_node.key)
        ),
    )


@given(strategies.non_empty_sets)
def test_accessing_in_order(set_: BaseSet[ValueT]) -> None:
    for value in set_:
        _ = value in set_

    tree = set_._tree
    assert to_height(tree) == to_max_binary_tree_height(tree)
