#!/usr/bin/env python3

from collections.abc import Sequence
from functools import cache as memoize
from typing import Any


def min_wt_triangulation(p: Sequence[tuple[float, float]], recursively: bool = False) -> float:
    # note: p is indexed from 0..(n-1) instead of 1..n

    n = len(p)

    @memoize
    def d(i: int, j: int) -> float:
        return sum((p[i][k] - p[j][k]) ** 2 for k in (0, 1)) ** 0.5

    T: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def T(i: int, j: int) -> float:
            return (
                d(i, j) if j == i + 1 else min(T(i, k) + T(k, j) + d(i, j) for k in range(i + 1, j))
            )

        return T(0, n - 1)
    else:
        T = {}
        for j_i in range(1, n):
            for i in range(n - j_i):
                j = i + j_i
                T[i, j] = (
                    d(i, j)
                    if j == i + 1
                    else min(T[i, k] + T[k, j] + d(i, j) for k in range(i + 1, j))
                )
        return T[0, n - 1]


def test_MWT() -> None:
    p1 = ((0, 0), (11, 1), (9, 8), (2, 6))
    p2 = ((0, 0), (1, 0), (1, 1), (0, 1))

    for p in (p1, p2):
        t1 = min_wt_triangulation(p)
        t2 = min_wt_triangulation(p, recursively=True)
        assert t1 == t2

    assert abs((t1 - 4) ** 2 - 2) <= 0.001


if __name__ == "__main__":
    for _ in range(1):
        test_MWT()

    print("test passed")
