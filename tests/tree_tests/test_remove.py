import pytest
from hypothesis import given
from lz.iterating import (first,
                          last)

from dendroid.binary import Tree
from dendroid.hints import Domain
from . import strategies


@given(strategies.empty_trees, strategies.totally_ordered_values)
def test_base_case(tree: Tree, value: Domain) -> None:
    with pytest.raises(KeyError):
        tree.remove(value)


@given(strategies.non_empty_trees)
def test_step_left(tree: Tree) -> None:
    value = first(tree)

    tree.remove(value)

    assert value not in tree


@given(strategies.non_empty_trees)
def test_step_right(tree: Tree) -> None:
    value = last(tree)

    tree.remove(value)

    assert value not in tree
