#!/usr/bin/env python3

from collections.abc import Sequence
from functools import cache as memoize
from typing import Any


def knapsack(w: Sequence[int], v: Sequence[float], L: int, recursively: bool = False) -> float:
    assert all(wi > 0 and isinstance(wi, int) for wi in w)
    assert all(vi >= 0 for vi in v)
    assert L >= 0 and isinstance(L, int)
    assert len(w) == len(v)

    n = len(w)

    V: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def V(i: int, ell: int) -> float:
            """max value achievable
            using first items {0,1,2,..,i-1}
            and total weight <= ell"""
            return (
                0
                if i == 0 or ell == 0
                else V(i - 1, ell)
                if w[i - 1] > ell
                else max(V(i - 1, ell), V(i - 1, ell - w[i - 1]) + v[i - 1])
            )

        return V(n, L)
    else:
        V = {}
        for i in range(n + 1):
            for ell in range(L + 1):
                V[i, ell] = (
                    0
                    if i == 0 or ell == 0
                    else V[i - 1, ell]
                    if w[i - 1] > ell
                    else max(V[i - 1, ell], V[i - 1, ell - w[i - 1]] + v[i - 1])
                )
        return V[n, L]


def test_knapsack(n: int = 10, L: int = 100) -> None:
    import random

    w = [random.randrange(1, 100) for _ in range(n)]
    v = [random.randrange(0, 100) for _ in range(n)]
    k1 = knapsack(w, v, L)
    k2 = knapsack(w, v, L, recursively=True)
    assert k1 == k2, (w, v, L, k1, k2)


if __name__ == "__main__":
    for _ in range(20):
        test_knapsack()

    print("test passed")
