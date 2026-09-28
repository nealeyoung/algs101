#!/usr/bin/env python3

from typing import Any, Protocol


class Ordered(Protocol):
    """a type whose values can be compared with < and >"""

    def __lt__(self, other: Any, /) -> bool: ...

    def __gt__(self, other: Any, /) -> bool: ...


def median[T: Ordered](A: list[T]) -> T:
    """return the median of the values in A"""

    return select(A, int((len(A) + 1) / 2))


def select[T: Ordered](A: list[T], k: int, randomized: bool = False) -> T:
    """return the kth smallest of the values in A"""

    n = len(A)
    assert 1 <= k <= n, (k, n)

    if randomized:
        if n == 1:
            return A[0]

        import random

        pivot = random.choice(A)

    else:
        if n < 15:
            return sorted(A)[k - 1]

        medians = [median(A[i : i + 5]) for i in range(0, n, 5)]
        pivot = median(medians)

    A1 = [a for a in A if a < pivot]
    A2 = [a for a in A if a == pivot]
    A3 = [a for a in A if a > pivot]

    if k <= len(A1):
        return select(A1, k)
    k -= len(A1)

    if k <= len(A2):
        return pivot
    k -= len(A2)

    return select(A3, k)


def test(n: int = 1000) -> None:
    import random

    A = [random.randrange(n) for _ in range(n)]
    k = 1 + random.randrange(n)
    kth = select(A, k)
    kth_r = select(A, k, randomized=True)

    B = sorted(A)
    assert B[k - 1] == kth == kth_r


for _ in range(50):
    test(200)

print("test passed")
