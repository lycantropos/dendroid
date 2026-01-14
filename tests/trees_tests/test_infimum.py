from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import NIL, Tree

from . import strategies


@given(strategies.trees_with_keys)
def test_properties(tree_with_key: tuple[Tree[KeyT, ValueT], KeyT]) -> None:
    tree, key = tree_with_key

    result = tree.infimum(key)

    assert (result is NIL and all(key < node.key for node in tree)) or (
        result is not NIL
        and not key < result.key
        and all(
            not node.key < key or node is result or node.key < result.key
            for node in tree
        )
    )
