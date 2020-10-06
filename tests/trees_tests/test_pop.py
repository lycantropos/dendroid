from typing import Tuple

from hypothesis import given

from dendroid.hints import Key
from tests.utils import (NIL,
                         Tree,
                         are_keys_equal,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.non_empty_trees_with_their_keys)
def test_properties(tree_with_key: Tuple[Tree, Key]) -> None:
    tree, key = tree_with_key

    tree.pop(key)

    assert (to_min_binary_tree_height(tree)
            <= to_height(tree)
            <= to_max_binary_tree_height(tree))
    assert is_left_subtree_less_than_right_subtree(tree)


@given(strategies.empty_trees_with_keys)
def test_base_case(tree_with_key: Tuple[Tree, Key]) -> None:
    tree, key = tree_with_key

    assert tree.pop(key) is NIL


@given(strategies.non_empty_trees_with_their_keys)
def test_step(tree_with_key: Tuple[Tree, Key]) -> None:
    tree, key = tree_with_key

    result = tree.pop(key)

    assert result not in tree
    assert are_keys_equal(result.key, key)
