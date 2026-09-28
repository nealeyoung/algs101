#!/usr/bin/env python3

from collections.abc import Collection, Hashable, Mapping
from functools import cache as memoize
from math import inf
from typing import Any

from graph_library import (
    in_neighbor_lists,
    random_digraph,
    random_weighted_digraph,
    topological_sort,
)


def count_paths[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    s: Vertex,
    t: Vertex,
    recursively: bool = False,
) -> int:
    in_neighbors = in_neighbor_lists(V, E)

    N: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def N(w: Vertex) -> int:
            return 1 if w == s else sum(N(u) for u in in_neighbors[w])

        return N(t)

    else:
        N = {}
        for w in topological_sort(V, E):
            N[w] = 1 if w == s else sum(N[u] for u in in_neighbors[w])
        return N[t]


def test_count_paths(n: int = 10, m: int | None = None) -> None:
    V, E = random_digraph(n, m, acyclic=True)
    n1 = count_paths(V, E, 0, n - 1)
    n2 = count_paths(V, E, 0, n - 1, recursively=True)
    assert n1 == n2


def shortest_path[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    s: Vertex,
    t: Vertex,
    recursively: bool = False,
) -> float:
    in_neighbors = in_neighbor_lists(V, E)

    D: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def D(w: Vertex) -> float:
            return (
                0 if w == s else min((D(u) + weights[u, w] for u in in_neighbors[w]), default=inf)
            )

        return D(t)

    else:
        D = {}
        for w in topological_sort(V, E):
            D[w] = (
                0 if w == s else min((D[u] + weights[u, w] for u in in_neighbors[w]), default=inf)
            )

        return D[t]


def longest_path[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    s: Vertex,
    t: Vertex,
    recursively: bool = False,
) -> float:
    in_neighbors = in_neighbor_lists(V, E)

    D: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def D(w: Vertex) -> float:
            return (
                0 if w == s else max((D(u) + weights[u, w] for u in in_neighbors[w]), default=-inf)
            )

        return D(t)

    else:
        D = {}
        for w in topological_sort(V, E):
            D[w] = (
                0 if w == s else max((D[u] + weights[u, w] for u in in_neighbors[w]), default=-inf)
            )

        return D[t]


def test_shortest_path(n: int = 10, m: int | None = None) -> None:
    V, E, weights = random_weighted_digraph(n, m, acyclic=True)
    d3 = shortest_path(V, E, weights, 0, n - 1)
    d4 = shortest_path(V, E, weights, 0, n - 1, recursively=True)
    assert d3 == d4


def test_longest_path(n: int = 10, m: int | None = None) -> None:
    V, E, weights = random_weighted_digraph(n, m, acyclic=True)
    d1 = longest_path(V, E, weights, 0, n - 1)
    d2 = longest_path(V, E, weights, 0, n - 1, recursively=True)

    weights = {e: -weights[e] for e in weights}
    d3 = shortest_path(V, E, weights, 0, n - 1)
    d4 = shortest_path(V, E, weights, 0, n - 1, recursively=True)

    assert d1 == d2 == -d3 == -d4


def make_change(denominations: Collection[int], target: int, recursively: bool = False) -> float:
    assert isinstance(target, int) and target >= 0
    assert all(isinstance(d, int) and d >= 1 for d in denominations)

    M: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def M(i: int) -> float:
            return (
                0 if i == 0 else min((1 + M(i - d) for d in denominations if d <= i), default=inf)
            )

        return M(target)

    else:
        M = {}
        for i in range(target + 1):
            M[i] = (
                0 if i == 0 else min((1 + M[i - d] for d in denominations if d <= i), default=inf)
            )
        return M[target]


def make_change_via_shortest_paths(denominations: Collection[int], target: int) -> float:
    assert isinstance(target, int) and target >= 0
    assert all(isinstance(d, int) and d >= 1 for d in denominations)

    V = range(target + 1)
    E = [(i, i + d) for i in V for d in denominations if i + d in V]
    weights = {e: 1 for e in E}
    return shortest_path(V, E, weights, 0, target)


def test_making_change(n: int = 10) -> None:
    import random

    assert n >= 1
    denominations = set(random.randrange(1, 25) for _ in range(5))
    target = random.randrange(n, 2 * n)
    d1 = make_change(denominations, target)
    d2 = make_change(denominations, target, recursively=True)
    d3 = make_change_via_shortest_paths(denominations, target)

    assert d1 == d2 == d3


if __name__ == "__main__":
    for _ in range(20):
        test_count_paths(50)
        test_shortest_path(50)
        test_longest_path(50)
        test_making_change()

    print("test passed")
