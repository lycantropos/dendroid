from collections import abc
from typing import (Callable,
                    Generic,
                    Iterable,
                    Iterator,
                    Optional,
                    Union)

from .abcs import (NIL,
                   Tree)
from .hints import (Item,
                    Key,
                    Value)
from .views import (BaseView,
                    ItemsView,
                    KeysView,
                    ValuesView)


@abc.MutableMapping.register
class Map(BaseView, Generic[Key, Value]):
    def __contains__(self, key: Key) -> bool:
        return self.tree.find(key) is not NIL

    def __delitem__(self, key: Key) -> None:
        self.tree.pop(key)

    def __getitem__(self, key: Key) -> Value:
        node = self.tree.find(key)
        if node is NIL:
            raise KeyError(key)
        return node.value

    def __iter__(self) -> Iterator[Key]:
        for node in self.tree:
            yield node.key

    def __len__(self) -> int:
        return len(self.tree)

    def __reversed__(self) -> Iterator[Key]:
        for node in reversed(self.tree):
            yield node.key

    def __setitem__(self, key: Key, value: Value) -> None:
        self.tree.insert(key, value).value = value

    def get(self,
            key: Key,
            default: Optional[Value] = None) -> Optional[Value]:
        node = self.tree.find(key)
        return default if node is NIL else node.value

    def clear(self) -> None:
        self.tree.clear()

    def items(self) -> ItemsView[Key, Value]:
        return ItemsView(self.tree)

    def keys(self) -> KeysView[Key]:
        return KeysView(self.tree)

    def max(self) -> Value:
        return self.tree.max().value

    def maxitem(self) -> Value:
        return self.tree.max().item

    def min(self) -> Value:
        return self.tree.max().value

    def minitem(self) -> Item:
        return self.tree.max().item

    __sentinel = object()

    def pop(self, key: Key, default: Value = __sentinel) -> Value:
        try:
            node = self.tree.pop(key)
        except KeyError:
            if default is self.__sentinel:
                raise
            return default
        else:
            return node.value

    def popmax(self) -> Value:
        return self.tree.popmax().value

    def popmaxitem(self) -> Value:
        return self.tree.popmax().item

    def popmin(self) -> Value:
        return self.tree.popmax().value

    def popminitem(self) -> Item:
        return self.tree.popmax().item

    popitem = popminitem

    def setdefault(self,
                   key: Key,
                   default: Optional[Value] = None) -> Optional[Value]:
        node = self.tree.find(key)
        return (self.tree.insert(key, default)
                if node is NIL
                else node).value

    def update(self,
               other: Union['Map[Key, Value]', Iterable[Item]] = ()) -> None:
        if isinstance(other, Map):
            for key in other:
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value

    def values(self) -> ValuesView[Value]:
        return ValuesView(self.tree)


def to_map_constructor(tree_constructor: Callable[..., Tree]
                       ) -> Callable[..., Map[Key, Value]]:
    def map_(*items: Item) -> Map[Key, Value]:
        return Map(tree_constructor(*zip(*items)))

    return map_
