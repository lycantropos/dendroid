from typing import (Any,
                    Callable)

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy
from lz.hints import Range

Strategy = SearchStrategy


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def builds_from(factories: Strategy[Callable[..., Range]],
                *args: Any,
                **kwargs: Any) -> Strategy[Range]:
    return factories.flatmap(lambda factory: strategies.builds(factory, *args,
                                                               **kwargs))
