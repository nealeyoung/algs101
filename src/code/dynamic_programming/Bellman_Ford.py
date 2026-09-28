#!/usr/bin/env python3

from collections.abc import Collection, Hashable, Mapping
from functools import cache as memoize
from math import inf
from typing import Any

from graph_library import in_neighbor_lists


def negative_cycles[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    d: Mapping[Vertex, float],
) -> bool:
    return any(d[w] > d[u] + weights[u, w] for (u, w) in E if d[u] != inf)


def check_negative_cycles[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    d: dict[Vertex, float],
) -> dict[Vertex, float] | None:
    return None if negative_cycles(V, E, weights, d) else d


def shortest_paths[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    s: Vertex,
    recursively: bool = False,
) -> dict[Vertex, float] | None:
    n = len(V)
    in_neighbors = in_neighbor_lists(V, E)

    M: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def M(w: Vertex, i: int) -> float:
            return (
                0
                if i == 0 and w == s
                else inf
                if i == 0 and w != s
                else min((M(u, i - 1) + weights[u, w] for u in in_neighbors[w]), default=inf)
            )

        d = {w: min(M(w, i) for i in range(n)) for w in V}
        return check_negative_cycles(V, E, weights, d)

    else:
        M = {}
        for i in range(n):
            for w in V:
                M[w, i] = (
                    0
                    if i == 0 and w == s
                    else inf
                    if i == 0 and w != s
                    else min(
                        (M[u, i - 1] + weights[u, w] for u in in_neighbors[w]),
                        default=inf,
                    )
                )
        d = {w: min(M[w, i] for i in range(n)) for w in V}
        return check_negative_cycles(V, E, weights, d)


def Bellman_Ford[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    s: Vertex,
) -> dict[Vertex, float] | None:
    n = len(V)
    in_neighbors = in_neighbor_lists(V, E)

    d: dict[Vertex, float] = {v: inf for v in V}
    d[s] = 0

    for _ in range(n):
        for w in V:
            d[w] = min(d[w], min((d[u] + weights[u, w] for u in in_neighbors[w]), default=inf))

    return check_negative_cycles(V, E, weights, d)


def check_shortest_path_distances[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    source: Vertex,
    d: Mapping[Vertex, float],
) -> bool:
    in_neighbors = in_neighbor_lists(V, E)

    return d[source] == 0 and all(
        d[w] == min((d[u] + weights[(u, w)] for u in in_neighbors[w]), default=inf)
        for w in V
        if w != source
    )


def test_shortest_paths(n: int, m: int, m_neg: int) -> int:
    import random

    from graph_library import random_weighted_digraph

    V, E, weights = random_weighted_digraph(n, m)
    for e in random.sample(E, m_neg):
        weights[e] *= -1
    source = 0

    d1 = Bellman_Ford(V, E, weights, source)
    d2 = shortest_paths(V, E, weights, source)
    d3 = shortest_paths(V, E, weights, source, recursively=True)

    assert d1 == d2 == d3, (d1, d2, d3)

    if d1:
        assert check_shortest_path_distances(V, E, weights, source, d1)
        return 1
    else:
        return 0


if __name__ == "__main__":
    n = 200
    m = int(n**1.25)
    T = 10
    count = 0
    for t in range(T):
        count += test_shortest_paths(n, m, int(0.15 * n * t / T))

    print("test passed, with", count, "of", T, "having no negative cycle")
