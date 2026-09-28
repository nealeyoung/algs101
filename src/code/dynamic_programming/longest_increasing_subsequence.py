#!/usr/bin/env python3


from collections.abc import Sequence
from functools import cache as memoize

from longest_common_subsequence import longest_common_subsequence


def longest_increasing_subsequence(A: Sequence[float], recursively: bool = False) -> int:
    n = len(A)

    if recursively:

        @memoize
        def LIS(j: int) -> int:
            return 1 + max((LIS(i) for i in range(j) if A[i] < A[j]), default=0)

        return max((LIS(i) for i in range(n)), default=0)

    else:
        L: dict[int, int] = {}
        for j in range(n):
            L[j] = 1 + max((L[i] for i in range(j) if A[i] < A[j]), default=0)
        return max((L[i] for i in range(n)), default=0)


def LIS_via_LCS(A: Sequence[float]) -> float:
    B = sorted(set(A))  # distinct values, so common subsequences are strictly increasing
    return longest_common_subsequence(A, B)


if __name__ == "__main__":

    def test_LIS(n: int = 10) -> None:
        import random

        A = [random.randrange(n) for _ in range(n)]
        L1 = longest_increasing_subsequence(A)
        L2 = longest_increasing_subsequence(A, recursively=True)
        L3 = LIS_via_LCS(A)
        assert L1 == L2 == L3

    for _ in range(20):
        test_LIS(50)

    print("test passed")
