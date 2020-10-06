from typing import Tuple

from hypothesis import given

from dendroid.hints import Key
from tests.utils import (NIL,
                         Tree)
from . import strategies


@given(strategies.trees_with_keys)
def test_properties(tree_with_key: Tuple[Tree, Key]) -> None:
    tree, key = tree_with_key

    result = tree.infimum(key)

    assert (result is NIL and all(key < node.key for node in tree)
            or not key < result.key)
