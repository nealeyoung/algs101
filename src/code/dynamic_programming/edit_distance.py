#!/usr/bin/env python3
# mypy: allow-redefinition

from collections.abc import Sequence
from functools import cache as memoize
from typing import Any

from dynamic_programming_paths import shortest_path


def edit_distance(A: Sequence[object], B: Sequence[object], recursively: bool = False) -> int:
    m, n = len(A), len(B)

    D: Any  # a memoized function if recursively, else a table (dict)
    if recursively:

        @memoize
        def D(i: int, j: int) -> int:
            return (
                max(i, j)
                if i == 0 or j == 0
                else D(i - 1, j - 1)
                if A[i - 1] == B[j - 1]
                else 1 + min(D(i, j - 1), D(i - 1, j), D(i - 1, j - 1))
            )

        return D(m, n)

    else:
        D = {}
        for i in range(m + 1):
            for j in range(n + 1):
                D[i, j] = (
                    max(i, j)
                    if i == 0 or j == 0
                    else D[i - 1, j - 1]
                    if A[i - 1] == B[j - 1]
                    else 1 + min(D[i, j - 1], D[i - 1, j], D[i - 1, j - 1])
                )
        return D[m, n]


def edit_distance_via_shortest_path(A: Sequence[object], B: Sequence[object]) -> float:
    m, n = len(A), len(B)

    vertices = [(i, j) for i in range(m + 1) for j in range(n + 1)]

    def match(i: int, j: int) -> bool:
        return i > 0 and j > 0 and A[i - 1] == B[j - 1]

    edges = (
        [((i - 1, j - 1), (i, j), int(not match(i, j))) for i, j in vertices]
        + [((i - 1, j), (i, j), 1) for i, j in vertices if not match(i, j)]
        + [((i, j - 1), (i, j), 1) for i, j in vertices if not match(i, j)]
    )
    weights = {(u, v): wt for u, v, wt in edges if min(u) >= 0}
    edges = weights.keys()
    return shortest_path(vertices, edges, weights, (0, 0), (m, n))


if __name__ == "__main__":

    def test_edit_distance(m: int = 10, n: int = 10) -> None:
        import random

        A = [random.randrange(m) for _ in range(m)]
        B = [random.randrange(n) for _ in range(n)]
        D1 = edit_distance(A, B)
        D2 = edit_distance(A, B, recursively=True)
        D3 = edit_distance_via_shortest_path(A, B)
        assert D1 == D2 == D3, (D1, D2, D3)

    for _ in range(15):
        test_edit_distance(30, 40)

    A, B = "SNOWY", "SUNNY"
    print("edit distance betweeen", A, "and", B, "is", edit_distance(A, B))
    print("test passed")
