#!/usr/bin/env python3

from collections.abc import Collection
from functools import cache as memoize
from math import inf
from typing import Any


def make_change(D: Collection[int], T: int, recursively: bool = False) -> float:
    assert all(d > 0 and isinstance(d, int) for d in D)
    assert T >= 0 and isinstance(T, int)

    m: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def m(t: int) -> float:
            """min coins to make change for t"""
            return 0 if t == 0 else min((1 + m(t - d) for d in D if d <= t), default=inf)

        return m(T)
    else:
        m = {}
        for t in range(T + 1):
            m[t] = 0 if t == 0 else min((1 + m[t - d] for d in D if d <= t), default=inf)
        return m[T]


def test_make_change(n: int = 10, T: int = 100) -> None:
    import random

    D = [random.randrange(1, 100) for _ in range(n)]
    m1 = make_change(D, T)
    m2 = make_change(D, T, recursively=True)
    assert m1 == m2


if __name__ == "__main__":
    for _ in range(20):
        test_make_change()

    print("test passed")
