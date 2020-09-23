from typing import Tuple

from hypothesis import given

from dendroid.hints import Key
from tests.utils import (KeysView,
                         are_keys_equal,
                         equivalence,
                         to_keys_view_including_key)
from . import strategies


@given(strategies.empty_keys_views_with_keys)
def test_base_case(keys_view_with_key: Tuple[KeysView, Key]) -> None:
    keys_view, key = keys_view_with_key

    assert key not in keys_view


@given(strategies.keys_views_with_keys_pairs)
def test_step(keys_view_with_keys_pair: Tuple[KeysView, Tuple[Key, Key]]
              ) -> None:
    keys_view, (extra_key, key) = keys_view_with_keys_pair

    next_keys_view = to_keys_view_including_key(keys_view, extra_key)

    assert equivalence(key in next_keys_view,
                       key in keys_view or are_keys_equal(key, extra_key))
