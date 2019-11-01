from typing import (List,
                    Optional)

from hypothesis import given

from dendroid.binary import (Tree,
                             tree)
from dendroid.hints import (Domain,
                            SortingKey)
from tests import strategies


@given(strategies.totally_ordered_values_lists, strategies.keys)
def test_basic(values: List[Domain], key: Optional[SortingKey]) -> None:
    result = tree(*values,
                  key=key)

    assert isinstance(result, Tree)
    assert len(result) <= len(values)
    assert all(value in result
               for value in values)
    assert all(value in values
               for value in result)


@given(strategies.totally_ordered_values_lists, strategies.keys)
def test_base_case(values: List[Domain], key: Optional[SortingKey]) -> None:
    result = tree(key=key)

    assert len(result) == 0
    assert all(value not in result
               for value in values)


@given(strategies.non_empty_totally_ordered_values_lists, strategies.keys)
def test_step(non_empty_values: List[Domain],
              key: Optional[SortingKey]) -> None:
    *values, value = non_empty_values

    result = tree(*values,
                  key=key)
    next_result = tree(*values, value,
                       key=key)

    assert next_result
    assert len(next_result) == len(result) + (value not in values)
    assert value in next_result
    assert all(value in next_result
               for value in result)
