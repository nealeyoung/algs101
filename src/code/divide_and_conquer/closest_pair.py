#!/usr/bin/env python3

from collections import namedtuple
from collections.abc import Iterable
from math import inf


def minf(*args: Iterable[float]) -> float:
    return min(*args, default=inf)


class Point(namedtuple("Point_", "x y")):
    def distance_squared(self, other: "Point") -> float:
        dx, dy = self.x - other.x, self.y - other.y
        return dx**2 + dy**2  # **0.5


def closest_pair(points: Iterable[tuple[float, float]]) -> float:
    """Return the square of the minimum Euclidean distance between any two of the given points"""

    points = list(points)
    P = set(Point(*p) for p in points)
    if len(P) < len(points):  # two equal points
        return 0.0
    Px = sorted(P, key=lambda p: p.x)
    Py = sorted(P, key=lambda p: p.y)

    def cp(Px: list[Point], Py: list[Point]) -> float:
        if len(Px) <= 1:
            return inf

        mid = int(len(Px) / 2)
        median_x = Px[mid].x

        Lx, Rx = Px[:mid], Px[mid:]
        L = set(Lx)
        Ly, Ry = [p for p in Py if p in L], [p for p in Py if p not in L]

        delta_L, delta_R = cp(Lx, Ly), cp(Rx, Ry)
        delta = min(delta_L, delta_R)

        My = [p for p in Py if (median_x - p.x) ** 2 < delta]
        delta_M = minf(p.distance_squared(q) for i, p in enumerate(My) for q in My[i + 1 : i + 9])
        return min(delta, delta_M)

    return cp(Px, Py)


def test_closest_pair(n: int = 30) -> None:
    import random

    P = [(2 * i, 2 * j) for i in range(n) for j in range(n)]
    (a, b) = random.choice(P)
    P += [(a + 1, b + 1)]

    assert abs(closest_pair(P) - 2) <= 1e-100


def test_closest_pair_small(n: int = 8) -> None:
    """Compare with brute force on a few random points."""
    import random
    from itertools import combinations

    P = [(random.random(), random.random()) for _ in range(random.randint(2, n))]
    brute_force = min(Point(*p).distance_squared(Point(*q)) for p, q in combinations(P, 2))
    assert abs(closest_pair(P) - brute_force) <= 1e-9, P


if __name__ == "__main__":
    for _ in range(10):
        test_closest_pair()
    for _ in range(200):
        test_closest_pair_small()

    print("test passed")
