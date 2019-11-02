from hypothesis import given

from dendroid.binary import Tree
from . import strategies


@given(strategies.trees)
def test_basic(tree: Tree) -> None:
    result = tree.clear()

    assert result is None
    assert len(tree) == 0