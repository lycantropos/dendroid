from hypothesis import given

from tests.hints import KeyT
from tests.utils import (
    KeysView,
    KeysViewsPair,
    KeysViewsTriplet,
    equivalence,
    is_left_subtree_less_than_right_subtree,
    to_height,
    to_max_binary_tree_height,
    to_min_binary_tree_height,
)

from . import strategies


@given(strategies.keys_views_pairs)
def test_type(keys_views_pair: KeysViewsPair[KeyT]) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view - right_keys_view

    assert isinstance(result, KeysView)


@given(strategies.keys_views_pairs)
def test_properties(keys_views_pair: KeysViewsPair[KeyT]) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view - right_keys_view

    result_tree = result.tree
    assert len(result) <= len(left_keys_view)
    assert (
        to_min_binary_tree_height(result_tree)
        <= to_height(result_tree)
        <= to_max_binary_tree_height(result_tree)
    )
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.keys_views)
def test_self_inverse(keys_view: KeysView[KeyT]) -> None:
    result = keys_view - keys_view

    assert len(result) == 0


@given(strategies.empty_keys_views_with_keys_views)
def test_left_absorbing_element(
    empty_tree_with_tree: KeysViewsPair[KeyT],
) -> None:
    empty_tree, keys_view = empty_tree_with_tree

    result = empty_tree - keys_view

    assert len(result) == 0


@given(strategies.empty_keys_views_with_keys_views)
def test_right_neutral_element(
    empty_tree_with_tree: KeysViewsPair[KeyT],
) -> None:
    empty_tree, keys_view = empty_tree_with_tree

    result = keys_view - empty_tree

    assert result == keys_view


@given(strategies.keys_views_pairs)
def test_expressing_intersection_as_difference(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view - (left_keys_view - right_keys_view)

    assert result == left_keys_view & right_keys_view


@given(strategies.keys_views_triplets)
def test_difference_subtrahend(
    keys_views_triplet: KeysViewsTriplet[KeyT],
) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = left_keys_view - (mid_tree - right_keys_view)

    assert result == (
        (left_keys_view - mid_tree) | (left_keys_view & right_keys_view)
    )


@given(strategies.keys_views_triplets)
def test_intersection_minuend(
    keys_views_triplet: KeysViewsTriplet[KeyT],
) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = (left_keys_view & mid_tree) - right_keys_view

    assert result == left_keys_view & (mid_tree - right_keys_view)


@given(strategies.keys_views_triplets)
def test_intersection_subtrahend(
    keys_views_triplet: KeysViewsTriplet[KeyT],
) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = left_keys_view - (mid_tree & right_keys_view)

    assert result == (
        (left_keys_view - mid_tree) | (left_keys_view - right_keys_view)
    )


@given(strategies.keys_views_triplets)
def test_union_subtrahend(keys_views_triplet: KeysViewsTriplet[KeyT]) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = left_keys_view - (mid_tree | right_keys_view)

    assert result == (
        (left_keys_view - mid_tree) & (left_keys_view - right_keys_view)
    )


@given(strategies.keys_views_pairs)
def test_connection_with_subkeys_view_relation(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view - right_keys_view

    assert result <= left_keys_view


@given(strategies.keys_views_pairs)
def test_connection_with_disjoint(
    keys_views_pair: KeysViewsPair[KeyT],
) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view - right_keys_view

    assert equivalence(
        left_keys_view.isdisjoint(right_keys_view), result == left_keys_view
    )
