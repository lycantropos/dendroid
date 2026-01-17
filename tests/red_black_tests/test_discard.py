from hypothesis import given

from tests.hints import ValueT
from tests.utils import (
    BaseSet,
    RedBlackTree,
    are_nodes_parents_to_children,
    do_paths_to_leaves_have_same_black_nodes_count,
    do_red_nodes_have_black_children,
    is_root_black,
)

from . import strategies


@given(strategies.sets_with_values)
def test_properties(set_with_value: tuple[BaseSet[ValueT], ValueT]) -> None:
    set_, value = set_with_value

    set_.discard(value)

    tree = set_._tree
    assert isinstance(tree, RedBlackTree)
    assert are_nodes_parents_to_children(tree)
    assert is_root_black(tree)
    assert do_red_nodes_have_black_children(tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(tree)
