from hypothesis import given

from dendroid import avl
from tests.utils import (are_balance_factors_normalized,
                         are_nodes_parents_to_children)
from . import strategies


@given(strategies.trees)
def test_properties(tree: avl.Tree) -> None:
    tree.clear()

    assert are_nodes_parents_to_children(tree)
    assert are_balance_factors_normalized(tree)