from hypothesis import given

from tests.utils import Tree
from . import strategies


@given(strategies.non_empty_trees)
def test_properties(tree: Tree) -> None:
    result = tree.min()

    assert tree._to_key(result) == tree.root.key
