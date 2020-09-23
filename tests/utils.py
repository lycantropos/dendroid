import math
import pickle
from functools import singledispatch
from itertools import (chain,
                       groupby,
                       islice)
from typing import (Any,
                    Callable,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    Sized,
                    Tuple,
                    TypeVar,
                    Union)

from hypothesis.strategies import SearchStrategy
from lz import left
from lz.functional import compose
from lz.iterating import interleave

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.core import abcs
from dendroid.core.abcs import Tree
from dendroid.core.maps import Map
from dendroid.core.sets import (BaseSet as Set,
                                KeyedSet)
from dendroid.core.utils import (are_keys_equal,
                                 to_balanced_tree_height)
from dendroid.core.views import KeysView
from dendroid.hints import (Key,
                            Order,
                            Value)

AnyNode = TypeVar('AnyNode', binary.Node, avl.Node, red_black.Node, splay.Node,
                  abcs.NIL)
Strategy = SearchStrategy
KeysView = KeysView
KeysViewsPair = Tuple[KeysView, KeysView]
KeysViewsTriplet = Tuple[KeysView, KeysView, KeysView]
Map = Map
MapsPair = Tuple[Map, Map]
Set = Set
SetsPair = Tuple[Set, Set]
SetsTriplet = Tuple[Set, Set, Set]
Tree = Tree
ValuesListWithOrder = Tuple[List[Value], Optional[Order]]
ValuesListsPairWithOrder = Tuple[List[Value], List[Value], Optional[Order]]
ValuesListsTripletWithOrder = Tuple[List[Value], List[Value], List[Value],
                                    Optional[Order]]
ValuesListsWithOrder = Union[ValuesListWithOrder, ValuesListsPairWithOrder,
                             ValuesListsTripletWithOrder]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def all_equal(iterable: Iterable[Any]) -> bool:
    groups = groupby(iterable)
    return next(groups, True) and not next(groups, False)


def one(iterable: Iterable[bool]) -> bool:
    iterator = iter(iterable)
    return any(iterator) and not any(iterator)


def pickle_round_trip(object_: Value) -> Value:
    return pickle.loads(pickle.dumps(object_))


def has_size_two_or_more(sized: Sized) -> bool:
    return len(sized) >= 2


def leap_traverse(values: List[Value]) -> List[Value]:
    return list(islice(interleave([values, reversed(values)]), len(values)))


are_keys_equal = are_keys_equal
to_balanced_tree_height = to_balanced_tree_height


def is_left_subtree_less_than_right_subtree(tree: Tree) -> bool:
    if tree.root is abcs.NIL:
        return True
    queue = [(tree.root, tree.min().key, tree.max().key)]
    while queue:
        node, left_end, right_end = queue.pop()
        if node.left is not abcs.NIL:
            if left_end <= node.left.key < right_end:
                queue.append((node.left, left_end, node.key))
            else:
                return False
        if node.right is not abcs.NIL:
            if node.key < node.right.key <= right_end:
                queue.append((node.right, node.key, right_end))
            else:
                return False
    return True


def are_nodes_parents_to_children(tree: Union[avl.Tree, red_black.Tree]
                                  ) -> bool:
    return all(is_node_parent_to_children(node)
               for node in iter_nodes(tree.root))


def is_node_parent_to_children(node: Union[avl.Node, red_black.Node]) -> bool:
    return _is_child_node(node.left, node) and _is_child_node(node.right, node)


def _is_child_node(node: Union[avl.Node, red_black.Node, abcs.NIL],
                   parent: Union[avl.Node, red_black.Node]) -> bool:
    return node is abcs.NIL or node.parent is parent


def to_height(tree: Tree) -> int:
    return to_node_height(tree.root)


def to_node_height(node: AnyNode) -> int:
    return (max(map(len, to_paths_to_leaves(node)),
                default=0)
            - 1)


to_min_binary_tree_height = compose(to_balanced_tree_height,
                                    len)  # type: Callable[[Tree], int]


@singledispatch
def to_max_binary_tree_height(tree: Tree) -> int:
    raise TypeError('Unsupported tree type: {type}.'
                    .format(type=type(tree)))


@to_max_binary_tree_height.register(binary.Tree)
@to_max_binary_tree_height.register(splay.Tree)
def _(tree: binary.Tree) -> int:
    return len(tree) - 1


MAX_AVL_TREE_HEIGHT_SLOPE = 1 / math.log2((1 + math.sqrt(5)) / 2)
MAX_AVL_TREE_HEIGHT_INTERCEPT = (MAX_AVL_TREE_HEIGHT_SLOPE * math.log2(5) / 2
                                 - 2)


@to_max_binary_tree_height.register(avl.Tree)
def _(tree: avl.Tree) -> int:
    return math.floor(MAX_AVL_TREE_HEIGHT_SLOPE * math.log2(len(tree) + 2)
                      + MAX_AVL_TREE_HEIGHT_INTERCEPT)


@to_max_binary_tree_height.register(red_black.Tree)
def _(tree: red_black.Tree) -> int:
    return 2 * to_balanced_tree_height(len(tree) + 1)


def are_balance_factors_normalized(tree: avl.Tree) -> bool:
    return all(node.balance_factor in (-1, 0, 1)
               for node in iter_nodes(tree.root))


def are_nodes_heights_correct(tree: avl.Tree) -> bool:
    return all(node.height == to_node_height(node)
               for node in iter_nodes(tree.root))


def is_root_black(tree: red_black.Tree) -> bool:
    return red_black._is_node_black(tree.root)


def do_red_nodes_have_black_children(tree: red_black.Tree) -> bool:
    return all(implication(not node.is_black,
                           red_black._is_node_black(node.left)
                           and red_black._is_node_black(node.right))
               for node in iter_nodes(tree.root))


def do_paths_to_leaves_have_same_black_nodes_count(tree: red_black.Tree
                                                   ) -> bool:
    return all(all_equal(to_black_nodes_count(path)
                         for path in to_paths_to_leaves(node))
               for node in iter_nodes(tree.root))


def to_black_nodes_count(path: Sequence[red_black.Node]) -> int:
    return sum(node.is_black for node in path)


def iter_nodes(root: AnyNode) -> Iterable[AnyNode]:
    if root is abcs.NIL:
        return
    queue = [root]
    while queue:
        node = queue.pop()
        yield node
        if node.left is not abcs.NIL:
            queue.append(node.left)
        if node.right is not abcs.NIL:
            queue.append(node.right)


def to_paths_to_leaves(root: AnyNode) -> Iterable[Sequence[AnyNode]]:
    if root is abcs.NIL:
        return
    queue = [[root]]
    while queue:
        path = queue.pop()
        last_node = path[-1]
        ended = True
        if last_node.left is not abcs.NIL:
            ended = False
            queue.append(path + [last_node.left])
        if last_node.right is not abcs.NIL:
            ended = False
            queue.append(path + [last_node.right])
        if ended:
            yield path


def map_value_to_key(map_: Map, value: Value) -> Key:
    return next(candidate_key
                for candidate_key, candidate_value in map_.items()
                if candidate_value is value)


def set_value_to_key(set_: Set, value: Value) -> Key:
    return set_.key(value) if isinstance(set_, KeyedSet) else value


def to_keys_view_including_key(keys_view: KeysView[Key],
                               key: Key) -> KeysView[Key]:
    return keys_view.from_iterable(chain(keys_view, (key,)))


def to_set_including_value(set_: Set, value: Value) -> Set:
    return set_.from_iterable(left.attach(set_, value))
