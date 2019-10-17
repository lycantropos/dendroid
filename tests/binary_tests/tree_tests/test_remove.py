import pytest
from hypothesis import given

from dendroid.binary import Tree
from dendroid.hints import Domain
from . import strategies


@given(strategies.empty_trees, strategies.totally_ordered_values)
def test_empty_tree(tree: Tree, value: Domain) -> None:
    with pytest.raises(KeyError):
        tree.remove(value)
