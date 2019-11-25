from functools import (partial,
                       wraps)
from typing import (Callable,
                    Tuple)

from hypothesis import strategies

from dendroid import (avl,
                      binary,
                      red_black,
                      splay)
from dendroid.hints import Domain
from tests.strategies import (empty_values_lists_with_keys,
                              non_empty_values_lists_with_keys,
                              single_values_with_keys,
                              to_values_lists_with_keys,
                              two_or_more_values_with_keys,
                              values_lists_with_keys,
                              values_with_keys_strategies)
from tests.utils import (Strategy,
                         Tree,
                         TreesPair,
                         TreesTriplet,
                         ValuesListWithKey,
                         ValuesListsPairWithKey,
                         ValuesListsTripletWithKey)


def to_degenerate_factory(factory: Callable[..., Tree]) -> Callable[..., Tree]:
    @wraps(factory)
    def wrapper(*values, key=None) -> Tree:
        result = factory(key=key)
        for value in values:
            result.add(value)
        return result

    return wrapper


factories = strategies.sampled_from([binary.tree, avl.tree, red_black.tree,
                                     splay.tree])
factories |= factories.map(to_degenerate_factory)


def to_tree(factory: Callable[..., Tree],
            values_list_with_key: ValuesListWithKey) -> Tree:
    values_list, key = values_list_with_key
    return factory(*values_list,
                   key=key)


empty_trees = strategies.builds(to_tree, factories,
                                empty_values_lists_with_keys)
trees = strategies.builds(to_tree, factories, values_lists_with_keys)


def to_empty_tree_with_tree(tree: Tree) -> TreesPair:
    return to_empty_copy(tree), tree


def to_empty_copy(tree: Tree) -> Tree:
    return tree.from_iterable((),
                              key=tree.key)


empty_trees_with_trees = trees.map(to_empty_tree_with_tree)
non_empty_trees = strategies.builds(to_tree, factories,
                                    non_empty_values_lists_with_keys)


def to_tree_with_value(factory: Callable[..., Tree],
                       values_list_with_key: ValuesListWithKey
                       ) -> Tuple[Tree, Domain]:
    values_list, key = values_list_with_key
    *rest_values_list, value = values_list
    tree = factory(*rest_values_list,
                   key=key)
    return tree, value


trees_with_values = strategies.builds(to_tree_with_value, factories,
                                      non_empty_values_lists_with_keys)
empty_trees_with_values = strategies.builds(to_tree_with_value, factories,
                                            single_values_with_keys)
non_empty_trees_with_values = strategies.builds(to_tree_with_value, factories,
                                                two_or_more_values_with_keys)


def to_non_empty_trees_with_their_values(tree: Tree
                                         ) -> Strategy[Tuple[Tree, Domain]]:
    return strategies.tuples(strategies.just(tree),
                             strategies.sampled_from(list(tree)))


non_empty_trees_with_their_values = (
    non_empty_trees.flatmap(to_non_empty_trees_with_their_values))


def to_trees_pair(factory: Callable[..., Tree],
                  values_lists_pair_with_key: ValuesListsPairWithKey
                  ) -> TreesPair:
    first_values_list, second_values_list, key = values_lists_pair_with_key
    first_tree = factory(*first_values_list,
                         key=key)
    second_tree = factory(*second_values_list,
                          key=key)
    return first_tree, second_tree


trees_pairs = strategies.builds(to_trees_pair,
                                factories,
                                values_with_keys_strategies
                                .flatmap(partial(to_values_lists_with_keys,
                                                 sizes=[(0, None)] * 2)))


def to_trees_triplet(factory: Callable[..., Tree],
                     values_lists_triplet_with_key: ValuesListsTripletWithKey
                     ) -> TreesTriplet:
    (first_values_list, second_values_list,
     third_values_list, key) = values_lists_triplet_with_key
    first_tree = factory(*first_values_list,
                         key=key)
    second_tree = factory(*second_values_list,
                          key=key)
    third_tree = factory(*third_values_list,
                         key=key)
    return first_tree, second_tree, third_tree


trees_triplets = strategies.builds(to_trees_triplet, factories,
                                   (values_with_keys_strategies
                                    .flatmap(partial(to_values_lists_with_keys,
                                                     sizes=[(0, None)] * 3))))


def to_trees_pair_with_value(factory: Callable[..., Tree],
                             values_lists_pair_with_key: ValuesListsPairWithKey
                             ) -> Tuple[Tree, Tree, Domain]:
    first_values_list, second_values_list, key = values_lists_pair_with_key
    *first_values_list, value = first_values_list
    first_tree = factory(*first_values_list,
                         key=key)
    second_tree = factory(*second_values_list,
                          key=key)
    return first_tree, second_tree, value


trees_pairs_with_values = (
    strategies.builds(to_trees_pair_with_value,
                      factories,
                      values_with_keys_strategies
                      .flatmap(partial(to_values_lists_with_keys,
                                       sizes=[(1, None), (0, None)]))))
