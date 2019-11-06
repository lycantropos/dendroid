from itertools import groupby
from typing import (Any,
                    Iterable,
                    Sequence,
                    Tuple,
                    TypeVar)

from hypothesis.searchstrategy import SearchStrategy

from dendroid import (binary,
                      red_black)

AnyNode = TypeVar('AnyNode', binary.Node, red_black.Node)
Strategy = SearchStrategy
Tree = binary.TreeBase
TreesPair = Tuple[Tree, Tree]
TreesTriplet = Tuple[Tree, Tree, Tree]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def all_equal(iterable: Iterable[Any]) -> bool:
    groups = groupby(iterable)
    return next(groups, True) and not next(groups, False)


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


def to_height(tree: Tree) -> int:
    return max(map(len, to_paths_to_leaves(tree.root)),
               default=0)


def is_root_black(tree: red_black.Tree) -> bool:
    return red_black._is_node_black(tree.root)


def do_red_nodes_have_black_children(tree: red_black.Tree) -> bool:
    return all(implication(not node.is_black,
                           red_black._is_node_black(node.left)
                           and red_black._is_node_black(node.right))
               for node in iter_nodes(tree.root))


def do_paths_to_leaves_have_same_black_nodes_count(
        tree: red_black.Tree) -> bool:
    return all(all_equal(to_black_nodes_count(path)
                         for path in to_paths_to_leaves(node))
               for node in iter_nodes(tree.root))


def to_black_height(tree: red_black.Tree) -> int:
    return max(to_paths_to_leaves(tree.root),
               key=len)


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


def log2ceil(number: int) -> int:
    return number.bit_length()
