from typing import TypeVar

from dendroid._core.hints import Ordered

Domain = TypeVar('Domain')
KeyT = TypeVar('KeyT', bound=Ordered)
ValueT = TypeVar('ValueT')
OrderedValueT = TypeVar('OrderedValueT', bound=Ordered)
Range = TypeVar('Range')
