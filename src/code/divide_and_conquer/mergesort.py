#!/usr/bin/env python3

from collections.abc import Iterator
from typing import Any, Protocol


class Ordered(Protocol):
    """a type whose values can be compared with <"""

    def __lt__(self, other: Any, /) -> bool: ...


def mergesort[T: Ordered](A: list[T]) -> list[T]:
    n = len(A)

    if n <= 1:
        return A

    m = int((n + 1) / 2)
    L = mergesort(A[:m])
    R = mergesort(A[m:])
    return list(merged(L, R))


def merged[T: Ordered](L: list[T], R: list[T]) -> Iterator[T]:
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            yield L[i]
            i += 1
        else:
            yield R[j]
            j += 1
    yield from L[i:] + R[j:]


def test(n: int = 1000) -> None:
    import random

    A = [random.randrange(n) for _ in range(n)]
    B = mergesort(A)
    C = sorted(A)
    assert B == C


for _ in range(50):
    test(200)

print("test passed")
