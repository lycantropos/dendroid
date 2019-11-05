from typing import (Any,
                    Callable,
                    Iterable,
                    Sequence,
                    Tuple,
                    TypeVar)

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy
from lz.hints import Range

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


def builds_from(factories: Strategy[Callable[..., Range]],
                *args: Any,
                **kwargs: Any) -> Strategy[Range]:
    return factories.flatmap(lambda factory: strategies.builds(factory, *args,
                                                               **kwargs))


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
