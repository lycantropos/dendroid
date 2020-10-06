from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import strategies

from dendroid import splay
from dendroid.hints import (Order,
                            Value)
from tests.strategies import (non_empty_values_lists_with_orders,
                              to_non_empty_sets_with_their_values,
                              two_or_more_values_with_orders,
                              values_lists_with_orders)
from tests.utils import (BaseSet,
                         ValuesListWithOrder)


def to_set(values_list_with_order: Tuple[List[Value], Optional[Order]]
           ) -> BaseSet:
    values_list, order = values_list_with_order
    return splay.set_(*values_list,
                      key=order)


sets = strategies.builds(to_set, values_lists_with_orders)
non_empty_sets = strategies.builds(to_set, non_empty_values_lists_with_orders)
non_empty_sets_with_their_values = (
    non_empty_sets.flatmap(to_non_empty_sets_with_their_values))


def is_value_non_max(set_with_value: Tuple[BaseSet, Value]) -> bool:
    set_, value = set_with_value
    return value != set_.max()


non_empty_sets_with_their_non_max_values = (non_empty_sets_with_their_values
                                            .filter(is_value_non_max))


def is_value_non_min(set_with_value: Tuple[BaseSet, Value]) -> bool:
    tree, value = set_with_value
    return value != tree.min()


non_empty_sets_with_their_non_min_values = (non_empty_sets_with_their_values
                                            .filter(is_value_non_min))


def to_set_with_value(values_list_with_order: ValuesListWithOrder
                      ) -> Tuple[BaseSet, Value]:
    values_list, order = values_list_with_order
    *rest_values_list, value = values_list
    set_ = splay.set_(*rest_values_list,
                      key=order)
    return set_, value


sets_with_values = strategies.builds(to_set_with_value,
                                     non_empty_values_lists_with_orders)
non_empty_sets_with_values = strategies.builds(to_set_with_value,
                                               two_or_more_values_with_orders)
