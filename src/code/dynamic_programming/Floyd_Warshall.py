#!/usr/bin/env python3

from collections.abc import Collection, Hashable, Mapping
from functools import cache as memoize
from math import inf
from typing import Any


def Floyd_Warshall[Vertex: Hashable](
    V: Collection[Vertex],
    E: Collection[tuple[Vertex, Vertex]],
    weights: Mapping[tuple[Vertex, Vertex], float],
    recursively: bool = False,
) -> dict[tuple[Vertex, Vertex], float]:
    n = len(V)
    V = list(V)
    E = set(E)

    M: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def M(u: Vertex, w: Vertex, i: int) -> float:
            return (
                0
                if u == w
                else weights[u, w]
                if i == 0 and (u, w) in E
                else inf
                if i == 0
                else min(M(u, w, i - 1), M(u, V[i - 1], i - 1) + M(V[i - 1], w, i - 1))
            )

        return {(u, w): M(u, w, n) for u in V for w in V}

    else:
        M = {}

        for i in range(n + 1):
            for u in V:
                for w in V:
                    M[u, w, i] = (
                        0
                        if u == w
                        else weights[u, w]
                        if i == 0 and (u, w) in E
                        else inf
                        if i == 0
                        else min(M[u, w, i - 1], M[u, V[i - 1], i - 1] + M[V[i - 1], w, i - 1])
                    )
        return {(u, w): M[u, w, n] for u in V for w in V}


def test_FW(n: int = 10, m: int | None = None) -> None:
    from graph_library import random_weighted_digraph

    V, E, weights = random_weighted_digraph(n, m)
    d1 = Floyd_Warshall(V, E, weights)
    d2 = Floyd_Warshall(V, E, weights, recursively=True)
    assert d1 == d2


if __name__ == "__main__":
    for _ in range(20):
        test_FW(50)

    print("test passed")
