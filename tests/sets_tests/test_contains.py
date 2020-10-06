from typing import Tuple

from hypothesis import given

from dendroid.hints import Value
from tests.utils import (BaseSet,
                         are_keys_equal,
                         equivalence,
                         set_value_to_key,
                         to_set_including_value)
from . import strategies


@given(strategies.empty_sets_with_values)
def test_base_case(set_with_value: Tuple[BaseSet, Value]) -> None:
    set_, value = set_with_value

    assert value not in set_


@given(strategies.sets_with_values_pairs)
def test_step(set_with_values_pair: Tuple[BaseSet, Tuple[Value, Value]]
              ) -> None:
    set_, (extra_value, value) = set_with_values_pair

    next_set = to_set_including_value(set_, extra_value)

    assert equivalence(value in next_set,
                       value in set_
                       or are_keys_equal(set_value_to_key(set_, value),
                                         set_value_to_key(set_, extra_value)))
