#!/usr/bin/env python3

from collections.abc import Iterator, Sequence
from functools import cache as memoize
from typing import Any


def paragraph_layout(N: int, w: Sequence[str], recursively: bool = False) -> int:
    """return min cost of any width-N layout of w"""

    # note: w is indexed from 0..(n-1) instead of 1..n

    assert all(len(wi) <= N for wi in w)

    n = len(w)

    @memoize
    def width(i: int, j: int) -> int:
        """return width of line with words w[i..j]"""
        assert 0 <= i <= j <= n - 1
        return len(w[i]) + (0 if i == j else 1 + width(i + 1, j))

    def i_range(j: int) -> Iterator[int]:
        """return range of i's s.t. width(i, j) <= N, in time O(j-i)"""
        assert 0 <= j <= n - 1
        i = j
        while i >= 0 and width(i, j) <= N:
            yield i
            i -= 1

    M: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def M(j: int) -> int:
            """min cost of layout of w[0...j]"""
            return 0 if j == -1 else min(M(i - 1) + (N - width(i, j)) ** 2 for i in i_range(j))

        return M(n - 1)
    else:
        M = {}
        M[-1] = 0
        for j in range(n):
            M[j] = min(M[i - 1] + (N - width(i, j)) ** 2 for i in i_range(j))
        return M[n - 1]


def test_paragraph_layout(N: int = 15, n: int = 10) -> None:
    import random

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    words = [random.choice(alphabet) * random.randrange(2, 6) for _ in range(n)]
    c1 = paragraph_layout(N, words)
    c2 = paragraph_layout(N, words, recursively=True)
    assert c1 == c2

    c1 = paragraph_layout(6, ["aaa", "bb", "cc", "dddd"])
    assert c1 == 14, c1


if __name__ == "__main__":
    for _ in range(20):
        test_paragraph_layout()

    print("test passed")
