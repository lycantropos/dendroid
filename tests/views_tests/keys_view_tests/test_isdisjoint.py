from hypothesis import given

from tests.hints import KeyT
from tests.utils import (
    KeysView,
    KeysViewsPair,
    equivalence,
    implication,
    to_keys_view_including_key,
)

from . import strategies


@given(strategies.keys_views_pairs)
def test_type(keys_views_pair: KeysViewsPair[KeyT]) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    result = first_keys_view.isdisjoint(second_keys_view)

    assert isinstance(result, bool)


@given(strategies.empty_keys_views_with_keys_views)
def test_base_case(
    empty_keys_view_with_keys_view: KeysViewsPair[KeyT],
) -> None:
    empty_keys_view, keys_view = empty_keys_view_with_keys_view

    assert empty_keys_view.isdisjoint(keys_view)


@given(strategies.keys_views_pairs_with_keys)
def test_step(
    two_keys_views_with_value: tuple[KeysView[KeyT], KeysView[KeyT], KeyT],
) -> None:
    left_keys_view, right_keys_view, key = two_keys_views_with_value

    next_left_keys_view = to_keys_view_including_key(left_keys_view, key)

    assert implication(
        not left_keys_view.isdisjoint(right_keys_view),
        not next_left_keys_view.isdisjoint(right_keys_view),
    )
    assert implication(
        left_keys_view.isdisjoint(right_keys_view),
        equivalence(
            next_left_keys_view.isdisjoint(right_keys_view),
            key not in right_keys_view,
        ),
    )


@given(strategies.keys_views_pairs)
def test_symmetry(keys_views_pair: KeysViewsPair[KeyT]) -> None:
    first_keys_view, second_keys_view = keys_views_pair

    assert equivalence(
        first_keys_view.isdisjoint(second_keys_view),
        second_keys_view.isdisjoint(first_keys_view),
    )
