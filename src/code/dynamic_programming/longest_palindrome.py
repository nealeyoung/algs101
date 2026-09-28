#!/usr/bin/env python3

from collections.abc import Sequence
from functools import cache as memoize
from typing import Any


def longest_palindromic_subsequence(X: Sequence[object], recursively: bool = False) -> int:
    n = len(X)

    M: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def M(i: int, j: int) -> int:
            return (
                0
                if j < i
                else 1
                if j == i
                else 2 + M(i + 1, j - 1)
                if j > i and X[i - 1] == X[j - 1]
                else max(M(i, j - 1), M(i + 1, j))
            )

        return M(1, n)

    else:
        M = {}
        for j in range(-1, n + 1):
            for i in range(j + 1, 0, -1):
                M[i, j] = (
                    0
                    if j < i
                    else 1
                    if j == i
                    else 2 + M[i + 1, j - 1]
                    if j > i and X[i - 1] == X[j - 1]
                    else max(M[i, j - 1], M[i + 1, j])
                )
        return M[1, n]


if __name__ == "__main__":

    def test(n: int = 10) -> None:
        import random

        X = [random.randrange(10) for _ in range(n)]
        l1 = longest_palindromic_subsequence(X)
        l2 = longest_palindromic_subsequence(X, recursively=True)
        assert l1 == l2

    def brute_force(X: Sequence[object]) -> int:
        from itertools import combinations

        return max(len(c) for r in range(len(X) + 1) for c in combinations(X, r) if c == c[::-1])

    def test_small(n: int = 8) -> None:
        import random

        X = [random.randrange(3) for _ in range(random.randrange(n + 1))]
        assert longest_palindromic_subsequence(X) == brute_force(X), X

    for _ in range(15):
        test(30)
    for _ in range(100):
        test_small()

    print("test passed")
