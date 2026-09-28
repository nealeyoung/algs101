#!/usr/bin/env python3

from collections.abc import Sequence
from functools import cache as memoize
from typing import Any


def optimal_BST(p: Sequence[float], recursively: bool = False) -> float:
    # note: p is indexed from 0..(n-1) instead of 1..n

    n = len(p)

    @memoize
    def wt(i: int, k: int) -> float:
        """return p[i-1] + p[i] + ... + p[k-1]"""
        return 0 if i > k else p[k - 1] + wt(i, k - 1)

    M: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def M(i: int, k: int) -> float:
            return (
                0 if i > k else min(wt(i, k) + M(i, j - 1) + M(j + 1, k) for j in range(i, k + 1))
            )

        return M(1, n)
    else:
        M = {}
        for k in range(n + 1):
            for i in range(k + 1, 0, -1):
                M[i, k] = (
                    0
                    if i > k
                    else min(wt(i, k) + M[i, j - 1] + M[j + 1, k] for j in range(i, k + 1))
                )
        return M[1, n]


def test_BST(n: int = 10) -> None:
    import random

    p = [random.randrange(n) for _ in range(n)]
    t1 = optimal_BST(p)
    t2 = optimal_BST(p, recursively=True)
    assert t1 == t2


if __name__ == "__main__":
    for _ in range(40):
        test_BST()

    print("test passed")
