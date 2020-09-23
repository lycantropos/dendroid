from typing import Tuple

from hypothesis import given

from tests.utils import (NIL,
                         Node,
                         Tree)
from . import strategies


@given(strategies.non_empty_trees_with_their_nodes)
def test_properties(tree_with_node: Tuple[Tree, Node]) -> None:
    tree, node = tree_with_node

    result = tree.successor(node)

    assert (result is NIL and (not tree or node is tree.max())
            or node.key < result.key)
