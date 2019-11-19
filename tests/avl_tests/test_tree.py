from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import given

from dendroid import avl
from dendroid.hints import (Domain,
                            SortingKey)
from dendroid.utils import to_balanced_tree_height
from tests import strategies
from tests.utils import (are_balance_factors_normalized,
                         are_nodes_parents_to_children,
                         is_left_subtree_less_than_right_subtree,
                         to_height)


@given(strategies.values_lists_with_keys)
def test_basic(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
               ) -> None:
    values, key = values_with_key

    result = avl.tree(*values,
                      key=key)

    assert isinstance(result, avl.Tree)


@given(strategies.values_lists_with_keys)
def test_properties(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                    ) -> None:
    values, key = values_with_key

    result = avl.tree(*values,
                      key=key)

    assert len(result) <= len(values)
    assert to_height(result) == to_balanced_tree_height(len(result))
    assert all(value in result
               for value in values)
    assert all(value in values
               for value in result)
    assert is_left_subtree_less_than_right_subtree(result)
    assert are_nodes_parents_to_children(result)
    assert are_balance_factors_normalized(result)


@given(strategies.values_lists_with_keys)
def test_base_case(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                   ) -> None:
    values, key = values_with_key

    result = avl.tree(key=key)

    assert len(result) == 0
    assert all(value not in result
               for value in values)


@given(strategies.non_empty_values_lists_with_keys)
def test_step(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
              ) -> None:
    values, key = values_with_key
    *values, value = values

    result = avl.tree(*values,
                      key=key)
    next_result = avl.tree(*values, value,
                           key=key)

    assert next_result
    assert len(next_result) == (len(result)
                                + (result._to_key(value)
                                   not in map(result._to_key, values)))
    assert value in next_result
    assert all(value in next_result
               for value in result)
