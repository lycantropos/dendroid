import math
from functools import singledispatch
from itertools import (groupby,
                       islice)
from typing import (Any,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    Tuple,
                    TypeVar,
                    Union)

from hypothesis.searchstrategy import SearchStrategy
from lz.functional import compose
from lz.iterating import interleave

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import (Domain,
                            SortingKey)
from dendroid.utils import to_balanced_tree_height

AnyNode = TypeVar('AnyNode', binary.Node, avl.Node, red_black.Node, splay.Node,
                  binary.NIL)
Strategy = SearchStrategy
Tree = binary.TreeBase
TreesPair = Tuple[Tree, Tree]
TreesTriplet = Tuple[Tree, Tree, Tree]
ValuesListWithKey = Tuple[List[Domain], Optional[SortingKey]]
ValuesListsPairWithKey = Tuple[List[Domain], List[Domain],
                               Optional[SortingKey]]
ValuesListsTripletWithKey = Tuple[List[Domain], List[Domain], List[Domain],
                                  Optional[SortingKey]]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def all_equal(iterable: Iterable[Any]) -> bool:
    groups = groupby(iterable)
    return next(groups, True) and not next(groups, False)


def leap_traverse(values: List[Domain]) -> List[Domain]:
    return list(islice(interleave([values, reversed(values)]), len(values)))


def is_left_subtree_less_than_right_subtree(tree: Tree) -> bool:
    if tree.root is binary.NIL:
        return True
    queue = [(tree.root, tree._to_key(tree.min()), tree._to_key(tree.max()))]
    while queue:
        node, left_end, right_end = queue.pop()
        if node.left is not binary.NIL:
            if left_end <= node.left.key < right_end:
                queue.append((node.left, left_end, node.key))
            else:
                return False
        if node.right is not binary.NIL:
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


def _is_child_node(node: Union[avl.Node, red_black.Node, binary.NIL],
                   parent: Union[avl.Node, red_black.Node]) -> bool:
    return node is binary.NIL or node.parent is parent


def to_height(tree: Tree) -> int:
    return to_node_height(tree.root)


def to_node_height(node: AnyNode) -> int:
    return (max(map(len, to_paths_to_leaves(node)),
                default=0)
            - 1)


to_min_binary_tree_height = compose(to_balanced_tree_height, len)


@singledispatch
def to_max_binary_tree_height(tree: binary.TreeBase) -> int:
    raise TypeError('Unsupported tree type: {type}.'
                    .format(type=type(tree)))


to_max_binary_tree_height.register(binary.Tree, len)

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


to_max_binary_tree_height.register(splay.Tree, len)


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
    if root is binary.NIL:
        return
    queue = [root]
    while queue:
        node = queue.pop()
        yield node
        if node.left is not binary.NIL:
            queue.append(node.left)
        if node.right is not binary.NIL:
            queue.append(node.right)


def to_paths_to_leaves(root: AnyNode) -> Iterable[Sequence[AnyNode]]:
    if root is binary.NIL:
        return
    queue = [[root]]
    while queue:
        path = queue.pop()
        last_node = path[-1]
        ended = True
        if last_node.left is not binary.NIL:
            ended = False
            queue.append(path + [last_node.left])
        if last_node.right is not binary.NIL:
            ended = False
            queue.append(path + [last_node.right])
        if ended:
            yield path
