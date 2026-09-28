#!/usr/bin/env python3
# mypy: allow-redefinition


from collections.abc import Sequence
from functools import cache as memoize

from dynamic_programming_paths import longest_path


def longest_common_subsequence(
    A: Sequence[object], B: Sequence[object], recursively: bool = False
) -> int:
    m, n = len(A), len(B)

    if recursively:

        @memoize
        def LCS(i: int, j: int) -> int:
            if 0 in {i, j}:
                return 0
            elif A[i - 1] == B[j - 1]:
                return 1 + LCS(i - 1, j - 1)
            else:
                return max(LCS(i, j - 1), LCS(i - 1, j))

        return LCS(m, n)

    else:
        L: dict[tuple[int, int], int] = {}
        for i in range(m + 1):
            for j in range(n + 1):
                if 0 in {i, j}:
                    L[i, j] = 0
                elif A[i - 1] == B[j - 1]:
                    L[i, j] = 1 + L[i - 1, j - 1]
                else:
                    L[i, j] = max(L[i, j - 1], L[i - 1, j])
        return L[m, n]


def LCS_via_longest_path(A: Sequence[object], B: Sequence[object]) -> float:
    m, n = len(A), len(B)

    vertices = [(i, j) for i in range(m + 1) for j in range(n + 1)]
    edges = (
        [((i - 1, j), (i, j), 0) for i, j in vertices]
        + [((i, j - 1), (i, j), 0) for i, j in vertices]
        + [
            ((i - 1, j - 1), (i, j), 1)
            for i, j in vertices
            if i > 0 and j > 0 and A[i - 1] == B[j - 1]
        ]
    )
    weights = {(u, v): wt for u, v, wt in edges if min(u) >= 0}
    edges = weights.keys()
    return longest_path(vertices, edges, weights, (0, 0), (m, n))


if __name__ == "__main__":

    def test_LCS(m: int = 10, n: int = 10) -> None:
        import random

        A = [random.randrange(m) for _ in range(m)]
        B = [random.randrange(n) for _ in range(n)]
        L1 = longest_common_subsequence(A, B)
        L2 = longest_common_subsequence(A, B, recursively=True)
        L3 = LCS_via_longest_path(A, B)
        assert L1 == L2 == L3

    for _ in range(20):
        test_LCS(50, 40)

    print("test passed")
