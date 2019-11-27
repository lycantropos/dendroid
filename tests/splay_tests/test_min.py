from hypothesis import given

from dendroid import splay
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: splay.Tree) -> None:
    result = tree.min()

    assert tree._to_key(result) == tree.root.key
