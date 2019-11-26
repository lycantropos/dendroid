from typing import Tuple

import pytest
from hypothesis import given

from dendroid.hints import Domain
from tests.utils import Tree
from . import strategies


@given(strategies.empty_trees_with_values)
def test_base_case(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    with pytest.raises(ValueError):
        tree.next(value)


@given(strategies.non_empty_trees_with_their_values)
def test_step(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    assert (value == tree.max()
            or tree._to_key(tree.next(value)) > tree._to_key(value))


@given(strategies.non_empty_trees)
def test_maximum(tree: Tree) -> None:
    maximum = tree.max()

    with pytest.raises(ValueError):
        tree.next(maximum)
