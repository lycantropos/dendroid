from typing import Tuple

from hypothesis import given

from dendroid.hints import Domain
from tests.utils import (Tree,
                         equivalence,
                         to_tree_including_value)
from . import strategies


@given(strategies.empty_trees_with_values)
def test_base_case(tree_with_value: Tuple[Tree, Domain]) -> None:
    tree, value = tree_with_value

    assert value not in tree


@given(strategies.trees_with_values_pairs)
def test_step(tree_with_values_pair: Tuple[Tree, Tuple[Domain, Domain]]
              ) -> None:
    tree, (extra_value, value) = tree_with_values_pair

    next_tree = to_tree_including_value(tree, extra_value)

    assert equivalence(value in next_tree,
                       value in tree
                       or tree._to_key(value) == tree._to_key(extra_value))
