from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import given

from dendroid import binary
from dendroid.hints import (Domain,
                            SortingKey)
from dendroid.utils import to_balanced_tree_height
from tests.utils import (is_left_subtree_less_than_right_subtree,
                         to_height)
from . import strategies


@given(strategies.values_lists_with_keys)
def test_basic(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
               ) -> None:
    values, key = values_with_key

    result = binary.tree(*values,
                         key=key)

    assert isinstance(result, binary.Tree)


@given(strategies.values_lists_with_keys)
def test_properties(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                    ) -> None:
    values, key = values_with_key

    result = binary.tree(*values,
                         key=key)

    assert len(result) <= len(values)
    assert to_height(result) == to_balanced_tree_height(len(result))
    assert all(value in result
               for value in values)
    assert all(value in values
               for value in result)
    assert is_left_subtree_less_than_right_subtree(result)


@given(strategies.values_lists_with_keys)
def test_base_case(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                   ) -> None:
    values, key = values_with_key

    result = binary.tree(key=key)

    assert len(result) == 0
    assert all(value not in result
               for value in values)


@given(strategies.non_empty_values_lists_with_keys)
def test_properties(values_with_key: Tuple[List[Domain], Optional[SortingKey]]
                    ) -> None:
    values, key = values_with_key
    *values, value = values

    result = binary.tree(*values,
                         key=key)
    next_result = binary.tree(*values, value,
                              key=key)

    assert next_result
    assert len(next_result) == (len(result)
                                + (result._to_key(value)
                                   not in map(result._to_key, values)))
    assert value in next_result
    assert all(value in next_result
               for value in result)
