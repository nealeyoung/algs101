#!/usr/bin/env python3

from collections.abc import Collection
from functools import cache as memoize
from typing import Any


def subset_sum(X: Collection[int], T: int, recursively: bool = False) -> bool:
    assert all(x >= 0 and isinstance(x, int) for x in X)
    assert T >= 0 and isinstance(T, int)

    X = list(X)
    n = len(X)

    S: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def S(i: int, t: int) -> bool:
            """is there a subset of the first j items summing to t ?"""
            return (
                True
                if t == 0 and i == 0
                else False
                if t > 0 and i == 0
                else S(i - 1, t) or S(i - 1, t - X[i - 1])
                if i > 0 and X[i - 1] <= t
                else S(i - 1, t)
            )

        return S(n, T)
    else:
        S = {}
        for i in range(n + 1):
            for t in range(T + 1):
                S[i, t] = (
                    True
                    if t == 0 and i == 0
                    else False
                    if t > 0 and i == 0
                    else S[i - 1, t] or S[i - 1, t - X[i - 1]]
                    if i > 0 and X[i - 1] <= t
                    else S[i - 1, t]
                )
        return S[n, T]


def test_subset_sum(n: int = 10, T: int = 100) -> None:
    import random

    X = [random.randrange(1, 100) for _ in range(n)]
    s1 = subset_sum(X, T)
    s2 = subset_sum(X, T, recursively=True)
    assert s1 == s2


if __name__ == "__main__":
    for _ in range(20):
        test_subset_sum()

    print("test passed")
