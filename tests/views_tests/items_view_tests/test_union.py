from hypothesis import given

from tests.utils import (ItemsView,
                         ItemsViewsPair,
                         ItemsViewsTriplet,
                         equivalence,
                         is_left_subtree_less_than_right_subtree,
                         to_height,
                         to_max_binary_tree_height,
                         to_min_binary_tree_height)
from . import strategies


@given(strategies.items_views_pairs)
def test_type(items_views_pair: ItemsViewsPair) -> None:
    left_items_view, right_items_view = items_views_pair

    result = left_items_view | right_items_view

    assert isinstance(result, ItemsView)


@given(strategies.items_views_pairs)
def test_properties(items_views_pair: ItemsViewsPair) -> None:
    left_items_view, right_items_view = items_views_pair

    result = left_items_view | right_items_view

    result_tree = result.tree
    assert len(result) <= len(left_items_view) + len(right_items_view)
    assert (to_min_binary_tree_height(result_tree)
            <= to_height(result_tree)
            <= min(to_height(left_items_view.tree)
                   + to_height(right_items_view.tree) + 1,
                   to_max_binary_tree_height(result_tree)))
    assert (all(value in result
                for value in left_items_view)
            and all(value in result
                    for value in right_items_view))
    assert ((not left_items_view or not result.isdisjoint(left_items_view))
            and (not right_items_view
                 or not result.isdisjoint(right_items_view)))
    assert is_left_subtree_less_than_right_subtree(result_tree)


@given(strategies.items_views)
def test_idempotence(items_view: ItemsView) -> None:
    result = items_view | items_view

    assert result == items_view


@given(strategies.empty_items_views_with_items_views)
def test_left_neutral_element(empty_tree_with_tree: ItemsViewsPair) -> None:
    empty_tree, items_view = empty_tree_with_tree

    result = empty_tree | items_view

    assert result == items_view


@given(strategies.empty_items_views_with_items_views)
def test_right_neutral_element(empty_tree_with_tree: ItemsViewsPair) -> None:
    empty_tree, items_view = empty_tree_with_tree

    result = items_view | empty_tree

    assert result == items_view


@given(strategies.items_views_pairs)
def test_absorption_identity(items_views_pair: ItemsViewsPair) -> None:
    left_items_view, right_items_view = items_views_pair

    result = left_items_view | (left_items_view & right_items_view)

    assert result == left_items_view


@given(strategies.items_views_pairs)
def test_commutativity(items_views_pair: ItemsViewsPair) -> None:
    left_items_view, right_items_view = items_views_pair

    result = left_items_view | right_items_view

    assert result == right_items_view | left_items_view


@given(strategies.items_views_triplets)
def test_associativity(items_views_triplet: ItemsViewsTriplet) -> None:
    left_items_view, mid_tree, right_items_view = items_views_triplet

    result = (left_items_view | mid_tree) | right_items_view

    assert result == left_items_view | (mid_tree | right_items_view)


@given(strategies.items_views_triplets)
def test_difference_operand(items_views_triplet: ItemsViewsTriplet) -> None:
    left_items_view, mid_tree, right_items_view = items_views_triplet

    result = (left_items_view - mid_tree) | right_items_view

    assert result == ((left_items_view | right_items_view)
                      - (mid_tree - right_items_view))


@given(strategies.items_views_triplets)
def test_distribution_over_intersection(items_views_triplet: ItemsViewsTriplet
                                        ) -> None:
    left_items_view, mid_tree, right_items_view = items_views_triplet

    result = left_items_view | (mid_tree & right_items_view)

    assert result == ((left_items_view | mid_tree)
                      & (left_items_view | right_items_view))


@given(strategies.items_views_pairs)
def test_connection_with_subitems_view_relation(items_views_pair: ItemsViewsPair
                                                ) -> None:
    left_items_view, right_items_view = items_views_pair

    result = left_items_view | right_items_view

    assert left_items_view <= result and right_items_view <= result


@given(strategies.items_views_pairs)
def test_connection_with_disjoint(items_views_pair: ItemsViewsPair) -> None:
    left_items_view, right_items_view = items_views_pair

    result = left_items_view | right_items_view

    assert equivalence(left_items_view.isdisjoint(right_items_view),
                       len(result)
                       == len(left_items_view) + len(right_items_view))
