from collections import abc

from hypothesis import given

from tests.hints import KeyT, ValueT
from tests.utils import Map

from . import strategies


@given(strategies.maps)
def test_type(map_: Map[KeyT, ValueT]) -> None:
    result = map_.values()

    assert isinstance(result, abc.Container)
    assert isinstance(result, abc.Iterable)
    assert isinstance(result, abc.Sized)


@given(strategies.maps)
def test_size(map_: Map[KeyT, ValueT]) -> None:
    result = map_.values()

    assert len(result) == len(map_)


@given(strategies.maps)
def test_elements(map_: Map[KeyT, ValueT]) -> None:
    result = map_.values()

    assert all(
        any(value is candidate for _, candidate in map_.items())
        for value in result
    )
    assert all(value in result for _, value in map_.items())
