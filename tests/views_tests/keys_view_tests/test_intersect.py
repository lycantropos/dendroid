from hypothesis import given

from tests.utils import (KeysView,
                         KeysViewsPair,
                         KeysViewsTriplet,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.keys_views_pairs)
def test_type(keys_views_pair: KeysViewsPair) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view & right_keys_view

    assert isinstance(result, type(left_keys_view))


@given(strategies.keys_views_pairs)
def test_properties(keys_views_pair: KeysViewsPair) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view & right_keys_view

    result_tree = result.tree
    assert len(result) <= min(len(left_keys_view), len(right_keys_view))
    assert (to_min_binary_tree_height(result_tree)
            <= to_height(result_tree)
            <= min(to_height(left_keys_view.tree),
                   to_height(right_keys_view.tree),
                   to_max_binary_tree_height(result_tree)))
    assert all(key in left_keys_view and key in right_keys_view
               for key in result)
    assert (not result
            or not result.isdisjoint(left_keys_view)
            and not result.isdisjoint(right_keys_view))
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.keys_views)
def test_idempotence(keys_view: KeysView) -> None:
    result = keys_view & keys_view

    assert result == keys_view


@given(strategies.empty_keys_views_with_keys_views)
def test_left_absorbing_element(empty_tree_with_tree: KeysViewsPair) -> None:
    empty_tree, keys_view = empty_tree_with_tree

    result = empty_tree & keys_view

    assert len(result) == 0
    assert not result


@given(strategies.empty_keys_views_with_keys_views)
def test_right_absorbing_element(empty_tree_with_tree: KeysViewsPair) -> None:
    empty_tree, keys_view = empty_tree_with_tree

    result = keys_view & empty_tree

    assert len(result) == 0
    assert not result


@given(strategies.keys_views_pairs)
def test_absorption_identity(keys_views_pair: KeysViewsPair) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view & (left_keys_view | right_keys_view)

    assert result == left_keys_view


@given(strategies.keys_views_pairs)
def test_commutativity(keys_views_pair: KeysViewsPair) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view & right_keys_view

    assert result == right_keys_view & left_keys_view


@given(strategies.keys_views_triplets)
def test_associativity(keys_views_triplet: KeysViewsTriplet) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = (left_keys_view & mid_tree) & right_keys_view

    assert result == left_keys_view & (mid_tree & right_keys_view)


@given(strategies.keys_views_triplets)
def test_difference_operand(keys_views_triplet: KeysViewsTriplet) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = (left_keys_view - mid_tree) & right_keys_view

    assert result == (left_keys_view & right_keys_view) - mid_tree


@given(strategies.keys_views_triplets)
def test_distribution_over_union(keys_views_triplet: KeysViewsTriplet) -> None:
    left_keys_view, mid_tree, right_keys_view = keys_views_triplet

    result = left_keys_view & (mid_tree | right_keys_view)

    assert result == ((left_keys_view & mid_tree)
                      | (left_keys_view & right_keys_view))


@given(strategies.keys_views_pairs)
def test_connection_with_subset_relation(keys_views_pair: KeysViewsPair
                                         ) -> None:
    left_keys_view, right_keys_view = keys_views_pair

    result = left_keys_view & right_keys_view

    assert result <= left_keys_view and result <= right_keys_view
