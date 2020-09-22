from typing import Tuple

from hypothesis import given

from tests.utils import (Set,
                         are_nodes_parents_to_children,
                         do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_root_black)
from . import strategies


@given(strategies.sets_pairs)
def test_properties(sets_pair: Tuple[Set, Set]) -> None:
    left_set, right_set = sets_pair

    result = left_set ^ right_set

    result_tree = result.tree
    assert are_nodes_parents_to_children(result_tree)
    assert is_root_black(result_tree)
    assert do_red_nodes_have_black_children(result_tree)
    assert do_paths_to_leaves_have_same_black_nodes_count(result_tree)
