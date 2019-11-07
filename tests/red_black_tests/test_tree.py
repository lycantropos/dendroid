from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import given

from dendroid import red_black
from dendroid.hints import (Domain,
                            SortingKey)
from tests import strategies
from tests.utils import (do_paths_to_leaves_have_same_black_nodes_count,
                         do_red_nodes_have_black_children,
                         is_left_subtree_less_than_right_subtree,
                         is_root_black,
                         to_height)
from dendroid.utils import log2ceil


@given(strategies.values_lists_with_keys)
def test_basic(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
               ) -> None:
    values, key = values_with_key

    result = red_black.tree(*values,
                            key=key)

    assert isinstance(result, red_black.Tree)


@given(strategies.values_lists_with_keys)
def test_properties(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                    ) -> None:
    values, key = values_with_key

    result = red_black.tree(*values,
                            key=key)

    assert len(result) <= len(values)
    assert to_height(result) == log2ceil(len(result))
    assert all(value in result
               for value in values)
    assert all(value in values
               for value in result)
    assert is_left_subtree_less_than_right_subtree(result)
    assert is_root_black(result)
    assert do_red_nodes_have_black_children(result)
    assert do_paths_to_leaves_have_same_black_nodes_count(result)


@given(strategies.values_lists_with_keys)
def test_base_case(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                   ) -> None:
    values, key = values_with_key

    result = red_black.tree(key=key)

    assert len(result) == 0
    assert all(value not in result
               for value in values)


@given(strategies.non_empty_values_lists_with_keys)
def test_step(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
              ) -> None:
    values, key = values_with_key
    *values, value = values

    result = red_black.tree(*values,
                            key=key)
    next_result = red_black.tree(*values, value,
                                 key=key)

    assert next_result
    assert len(next_result) == (len(result)
                                + (result._to_key(value)
                                   not in map(result._to_key, values)))
    assert value in next_result
    assert all(value in next_result
               for value in result)
