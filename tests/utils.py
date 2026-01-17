import math
import pickle
from collections import deque
from collections.abc import Callable, Iterable, Sequence, Sized
from functools import singledispatch
from itertools import chain, count, groupby
from operator import is_
from typing import Any, TypeAlias, TypeVar, overload

from typing_extensions import TypeIs

from dendroid._core import (
    abcs as _abcs,
    avl,
    binary,
    maps as _maps,
    nil as _nil,
    red_black,
    sets as _sets,
    splay,
    utils as _utils,
    views as _views,
)
from dendroid.hints import Item, Order
from tests.hints import Domain, KeyT, Range, ValueT

AnyNode: TypeAlias = (
    binary.Node[KeyT, ValueT]
    | avl.Node[KeyT, ValueT]
    | red_black.Node[KeyT, ValueT]
    | splay.Node[KeyT, ValueT]
    | _abcs.Node[KeyT, ValueT]
)
AnyNodeT = TypeVar(
    'AnyNodeT',
    binary.Node[Any, Any],
    avl.Node[Any, Any],
    red_black.Node[Any, Any],
    splay.Node[Any, Any],
    _abcs.Node[Any, Any],
)
ItemsView = _views.ItemsView
ItemsViewsPair: TypeAlias = tuple[
    ItemsView[KeyT, ValueT], ItemsView[KeyT, ValueT]
]
ItemsViewsTriplet: TypeAlias = tuple[
    ItemsView[KeyT, ValueT], ItemsView[KeyT, ValueT], ItemsView[KeyT, ValueT]
]
KeysView = _views.KeysView
KeysViewsPair: TypeAlias = tuple[KeysView[KeyT], KeysView[KeyT]]
KeysViewsTriplet: TypeAlias = tuple[
    KeysView[KeyT], KeysView[KeyT], KeysView[KeyT]
]
Map = _maps.Map
MapsPair: TypeAlias = tuple[Map[KeyT, ValueT], Map[KeyT, ValueT]]
Node = _abcs.Node[KeyT, ValueT]
BaseSet = _sets.BaseSet
BaseSetsPair: TypeAlias = tuple[BaseSet[ValueT], BaseSet[ValueT]]
BaseSetsTriplet: TypeAlias = tuple[
    BaseSet[ValueT], BaseSet[ValueT], BaseSet[ValueT]
]
Tree = _abcs.Tree
AvlTree = avl.Tree
RedBlackTree = red_black.Tree
TreesPair: TypeAlias = tuple[Tree[KeyT, ValueT], Tree[KeyT, ValueT]]
TreesTriplet: TypeAlias = tuple[
    Tree[KeyT, ValueT], Tree[KeyT, ValueT], Tree[KeyT, ValueT]
]
ValueSequenceWithOrder: TypeAlias = tuple[
    Sequence[ValueT], Order[ValueT, KeyT] | None
]
ValueSequencePairWithOrder: TypeAlias = tuple[
    tuple[Sequence[ValueT], Sequence[ValueT]], Order[ValueT, KeyT] | None
]
ValueSequencesWithOrder: TypeAlias = tuple[
    tuple[Sequence[ValueT], ...], Order[ValueT, KeyT] | None
]
ValuesView = _views.ValuesView
ValuesViewsPair: TypeAlias = tuple[ValuesView[ValueT], ValuesView[ValueT]]
ValuesViewsTriplet: TypeAlias = tuple[
    ValuesView[ValueT], ValuesView[ValueT], ValuesView[ValueT]
]

NIL = _nil.NIL
Nil = _nil.Nil


equivalence = is_


def implication(antecedent: bool, consequent: bool, /) -> bool:  # noqa: FBT001
    return not antecedent or consequent


def all_equal(iterable: Iterable[Any], /) -> bool:
    groups = groupby(iterable)
    return next(groups, True) and not next(groups, False)


def to_constant(value: ValueT, /) -> Callable[..., ValueT]:
    def constant(*_: Any, **__: Any) -> ValueT:
        return value

    return constant


def identity(value: ValueT, /) -> ValueT:
    return value


def capacity(iterable: Iterable[Any], /) -> int:
    counter = count()
    deque(zip(iterable, counter, strict=False), maxlen=0)
    return next(counter)


_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')
_U1 = TypeVar('_U1')
_U2 = TypeVar('_U2')


def combine(
    first_function: Callable[[_T1], _U1],
    second_function: Callable[[_T2], _U2],
    /,
) -> Callable[[tuple[_T1, _T2]], tuple[_U1, _U2]]:
    def combination(arguments: tuple[_T1, _T2], /) -> tuple[_U1, _U2]:
        first_argument, second_argument = arguments
        return first_function(first_argument), second_function(second_argument)

    return combination


def compose(
    last_function: Callable[..., Range], /, *rest_functions: Callable[..., Any]
) -> Callable[..., Range]:
    if len(rest_functions) == 0:
        return last_function
    *mid_functions, first_function = rest_functions
    mid_functions = mid_functions[::-1]

    def composition(*args: Domain, **kwargs: Domain) -> Range:
        result = first_function(*args, **kwargs)
        for function in mid_functions:
            result = function(result)
        return last_function(result)

    return composition


def first(iterable: Iterable[ValueT]) -> ValueT:
    try:
        return next(iter(iterable))
    except StopIteration as error:
        raise ValueError('Argument supposed to be non-empty.') from error


def last(iterable: Iterable[ValueT]) -> ValueT:
    try:
        return deque(iterable, maxlen=1)[0]
    except IndexError as error:
        raise ValueError('Argument supposed to be non-empty.') from error


def one(iterable: Iterable[bool]) -> bool:
    iterator = iter(iterable)
    return any(iterator) and not any(iterator)


def pairwise(iterable: Iterable[ValueT]) -> Iterable[tuple[ValueT, ValueT]]:
    iterator = iter(iterable)
    try:
        value = next(iterator)
    except StopIteration:
        return
    else:
        for next_value in iterator:
            yield value, next_value
            value = next_value


def pickle_round_trip(object_: Any, /) -> Any:
    return pickle.loads(pickle.dumps(object_))


def has_size_two_or_more(sized: Sized) -> bool:
    return len(sized) >= 2


def leap_traverse(values: Sequence[ValueT], /) -> Sequence[ValueT]:
    iterator, reversed_iterator = iter(values), reversed(values)
    result: list[ValueT] = []
    size_half, is_odd = divmod(len(values), 2)
    for _ in range(size_half):
        result.extend((next(iterator), next(reversed_iterator)))
    if is_odd:
        result.append(next(iterator))
    return result


are_keys_equal = _utils.are_keys_equal


def are_items_equal(
    left: Item[KeyT, ValueT], right: Item[KeyT, ValueT], /
) -> bool:
    left_key, left_value = left
    right_key, right_value = right
    return (
        _utils.are_keys_equal(left_key, right_key)
        and left_value == right_value
    )


def are_items_keys_equal(
    left: Item[KeyT, ValueT], right: Item[KeyT, ValueT], /
) -> bool:
    left_key, _ = left
    right_key, _ = right
    return _utils.are_keys_equal(left_key, right_key)


to_balanced_tree_height = _utils.to_balanced_tree_height


def is_left_subtree_less_than_right_subtree(
    tree: Tree[KeyT, ValueT], /
) -> bool:
    if tree.root is NIL:
        return True
    min_node = tree.min()
    assert min_node is not NIL
    max_node = tree.max()
    assert max_node is not NIL
    queue = [(tree.root, min_node.key, max_node.key)]
    while queue:
        node, left_end, right_end = queue.pop()
        if node.left is not NIL:
            if left_end <= node.left.key < right_end:
                queue.append((node.left, left_end, node.key))
            else:
                return False
        if node.right is not NIL:
            if node.key < node.right.key <= right_end:
                queue.append((node.right, node.key, right_end))
            else:
                return False
    return True


def are_nodes_parents_to_children(
    tree: avl.Tree[KeyT, ValueT] | red_black.Tree[KeyT, ValueT], /
) -> bool:
    return all(
        _is_node_with_parent(node) and _is_node_parent_to_its_children(node)
        for node in iter_nodes(tree.root)  # type: ignore[type-var]
    )


def _is_node_with_parent(
    node: Any, /
) -> TypeIs[avl.Node[KeyT, ValueT] | red_black.Node[KeyT, ValueT]]:
    return isinstance(node, avl.Node | red_black.Node)


def _is_node_parent_to_its_children(
    node: avl.Node[KeyT, ValueT] | red_black.Node[KeyT, ValueT], /
) -> bool:
    return _is_child_node(node.left, node) and _is_child_node(node.right, node)


def _is_child_node(
    node: avl.Node[KeyT, ValueT] | red_black.Node[KeyT, ValueT] | Nil,
    parent: avl.Node[KeyT, ValueT] | red_black.Node[KeyT, ValueT],
    /,
) -> bool:
    return node is NIL or node.parent is parent


def to_height(tree: Tree[KeyT, ValueT], /) -> int:
    return to_node_height(tree.root)


def to_node_height(node: AnyNode[KeyT, ValueT] | Nil, /) -> int:
    return max(map(len, to_paths_to_leaves(node)), default=0) - 1


def to_min_binary_tree_height(tree: Tree[KeyT, ValueT]) -> int:
    return _utils.to_balanced_tree_height(len(tree))


@singledispatch
def to_max_binary_tree_height(tree: Tree[KeyT, ValueT], /) -> int:
    raise TypeError(f'Unsupported tree type: {type(tree)}.')


@to_max_binary_tree_height.register(binary.Tree)
@to_max_binary_tree_height.register(splay.Tree)
def _(tree: binary.Tree[KeyT, ValueT], /) -> int:
    return len(tree) - 1


MAX_AVL_TREE_HEIGHT_SLOPE = 1 / math.log2((1 + math.sqrt(5)) / 2)
MAX_AVL_TREE_HEIGHT_INTERCEPT = (
    MAX_AVL_TREE_HEIGHT_SLOPE * math.log2(5) / 2 - 2
)


@to_max_binary_tree_height.register(avl.Tree)
def _(tree: avl.Tree[KeyT, ValueT], /) -> int:
    return math.floor(
        MAX_AVL_TREE_HEIGHT_SLOPE * math.log2(len(tree) + 2)
        + MAX_AVL_TREE_HEIGHT_INTERCEPT
    )


@to_max_binary_tree_height.register(red_black.Tree)
def _(tree: red_black.Tree[KeyT, ValueT], /) -> int:
    return 2 * _utils.to_balanced_tree_height(len(tree) + 1)


def are_balance_factors_normalized(tree: avl.Tree[KeyT, ValueT], /) -> bool:
    return all(
        node.balance_factor in (-1, 0, 1) for node in iter_nodes(tree.root)
    )


def are_nodes_heights_correct(tree: avl.Tree[KeyT, ValueT], /) -> bool:
    return all(
        node.height == to_node_height(node) for node in iter_nodes(tree.root)
    )


is_red_black_tree_node_black = red_black._is_node_black


def is_root_black(tree: red_black.Tree[KeyT, ValueT], /) -> bool:
    return is_red_black_tree_node_black(tree.root)


def do_red_nodes_have_black_children(
    tree: red_black.Tree[KeyT, ValueT], /
) -> bool:
    return all(
        implication(
            not node.is_black,
            is_red_black_tree_node_black(node.left)
            and is_red_black_tree_node_black(node.right),
        )
        for node in iter_nodes(tree.root)
    )


def do_paths_to_leaves_have_same_black_nodes_count(
    tree: red_black.Tree[KeyT, ValueT], /
) -> bool:
    return all(
        all_equal(
            to_black_nodes_count(path) for path in to_paths_to_leaves(node)
        )
        for node in iter_nodes(tree.root)
    )


def to_black_nodes_count(
    path: Sequence[red_black.Node[KeyT, ValueT]], /
) -> int:
    return sum(node.is_black for node in path)


def iter_nodes(root: AnyNodeT | Nil, /) -> Iterable[AnyNodeT]:
    if root is NIL:
        return
    queue = [root]
    while queue:
        node = queue.pop()
        yield node
        if node.left is not NIL:
            queue.append(node.left)
        if node.right is not NIL:
            queue.append(node.right)


def to_paths_to_leaves(
    root: AnyNodeT | Nil, /
) -> Iterable[Sequence[AnyNodeT]]:
    if root is NIL:
        return
    queue: list[tuple[AnyNodeT, ...]] = [(root,)]
    while queue:
        path = queue.pop()
        last_node = path[-1]
        ended = True
        if last_node.left is not NIL:
            ended = False
            queue.append(path + (last_node.left,))  # noqa: RUF005
        if last_node.right is not NIL:
            ended = False
            queue.append(path + (last_node.right,))  # noqa: RUF005
        if ended:
            yield path


def map_value_to_key(map_: Map[KeyT, ValueT], value: ValueT, /) -> Any:
    return next(
        candidate_key
        for candidate_key, candidate_value in map_.items()
        if candidate_value is value
    )


@overload
def set_value_to_key(
    set_: _sets.KeyedSet[KeyT, ValueT], value: ValueT, /
) -> KeyT: ...


@overload
def set_value_to_key(set_: _sets.Set[ValueT], value: ValueT, /) -> ValueT: ...


@overload
def set_value_to_key(set_: BaseSet[ValueT], value: ValueT, /) -> Any: ...


def set_value_to_key(set_: BaseSet[ValueT], value: ValueT, /) -> Any:
    return set_.key(value) if isinstance(set_, _sets.KeyedSet) else value


def to_items_view_including_item(
    items_view: ItemsView[KeyT, ValueT], item: Item[KeyT, ValueT], /
) -> ItemsView[KeyT, ValueT]:
    return items_view.from_iterable(chain(items_view, (item,)))


def to_keys_view_including_key(
    keys_view: KeysView[KeyT], key: KeyT, /
) -> KeysView[KeyT]:
    return keys_view.from_iterable(chain(keys_view, (key,)))


def to_set_including_value(
    set_: BaseSet[ValueT], value: ValueT, /
) -> BaseSet[ValueT]:
    return set_.from_iterable((*set_, value))
