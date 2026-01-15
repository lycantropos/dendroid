import math
import sys

from hypothesis import given

from tests.hints import KeyT
from tests.utils import KeysView

from . import strategies


@given(strategies.keys_views)
def test_evaluation(keys_view: KeysView[KeyT]) -> None:
    result = repr(keys_view)

    type_ = type(keys_view)
    # `math` module is required for `inf` object
    assert (
        eval(
            result, {**sys.modules}, {**vars(math), type_.__qualname__: type_}
        )
        == keys_view
    )
