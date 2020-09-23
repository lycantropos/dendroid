from hypothesis import given
from lz.iterating import (capacity,
                          pairwise)

from tests.utils import Tree
from . import strategies


@given(strategies.trees)
def test_size(tree: Tree) -> None:
    result = reversed(tree)

    assert capacity(result) == len(tree)


@given(strategies.trees)
def test_elements(tree: Tree) -> None:
    result = reversed(tree)

    assert all(element in tree for element in result)


@given(strategies.trees_with_two_or_more_nodes)
def test_order(tree: Tree) -> None:
    result = reversed(tree)

    assert all(next_node.key < node.key
               for node, next_node in pairwise(result))
