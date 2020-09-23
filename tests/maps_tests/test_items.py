from collections import abc

from hypothesis import given

from tests.utils import Map
from . import strategies


@given(strategies.maps)
def test_type(map_: Map) -> None:
    result = map_.items()

    assert isinstance(result, abc.Set)


@given(strategies.maps)
def test_size(map_: Map) -> None:
    result = map_.items()

    assert len(result) == len(map_)


@given(strategies.maps)
def test_elements(map_: Map) -> None:
    result = map_.items()

    assert all(any(item == candidate
                   for candidate in zip(map_.keys(), map_.values()))
               for item in result)
    assert all(item in result for item in zip(map_.keys(), map_.values()))
