import math
import sys

from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import ItemsView

from . import strategies


@given(strategies.items_views)
def test_evaluation(items_view: ItemsView[KeyT, ValueT]) -> None:
    result = repr(items_view)

    type_ = type(items_view)
    # `math` module is required for `inf` object
    assert (
        eval(result, sys.modules, {**vars(math), type_.__qualname__: type_})
        == items_view
    )
