from collections import abc

from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map, are_keys_equal

from . import strategies


@given(strategies.maps)
def test_type(map_: Map[KeyT, ValueT]) -> None:
    result = map_.keys()

    assert isinstance(result, abc.Set)


@given(strategies.maps)
def test_size(map_: Map[KeyT, ValueT]) -> None:
    result = map_.keys()

    assert len(result) == len(map_)


@given(strategies.maps)
def test_elements(map_: Map[KeyT, ValueT]) -> None:
    result = map_.keys()

    assert all(
        any(are_keys_equal(key, candidate) for candidate in map_)
        for key in result
    )
    assert all(key in result for key in map_)
