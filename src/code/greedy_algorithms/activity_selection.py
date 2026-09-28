#!/usr/bin/env python3

from collections.abc import Collection, Iterable, Sequence
from typing import NamedTuple


class Interval(NamedTuple):
    start: int
    finish: int

    def starts_after(self, other: "Interval") -> bool:
        return self.start > other.finish

    def empty(self) -> bool:
        return self.start > self.finish

    @staticmethod
    def random_interval(m: int) -> "Interval":
        import random

        return Interval(*sorted([random.randrange(m), random.randrange(m)]))

    @staticmethod
    def random_intervals(n: int, m: int = 0) -> list["Interval"]:
        if not n:
            return []

        if not m:
            m = 2 * n
        assert m > 0

        I: set[Interval] = set()
        while len(I) < n:
            I.add(Interval.random_interval(m))

        return sorted(I, key=lambda J: J.finish)


def rselect(I: list[Interval]) -> set[Interval]:
    if not I:
        return set()
    J1 = I[0]
    D = [J for J in I if J.starts_after(J1)]
    R = rselect(D)
    return {
        J1,
    } | R


def rselect_efficiently(I: list[Interval]) -> list[Interval]:
    result: list[Interval] = []

    def r(i: int) -> None:
        J1 = I[i]
        result.append(J1)
        for j in range(i + 1, len(I)):
            if I[j].starts_after(J1):
                r(j)
                return

    if I:
        r(0)

    return result


def iselect(I: list[Interval]) -> list[Interval]:
    X: list[Interval] = []
    for J in I:
        if not X or J.starts_after(X[-1]):
            X.append(J)

    return X


if __name__ == "__main__":

    def is_pairwise_disjoint(jobs: Iterable[Interval]) -> bool:
        jobs = sorted(jobs, key=lambda J: J.finish)
        return all(J2.starts_after(J1) for J1, J2 in zip(jobs, jobs[1:]))

    def is_sorted_by_finish_time(jobs: Sequence[Interval]) -> bool:
        return all(J1.finish <= J2.finish for J1, J2 in zip(jobs, jobs[1:]))

    def test() -> None:
        I = Interval.random_intervals(1000)
        assert is_sorted_by_finish_time(I)
        assert all(not J.empty() for J in I)

        solns: list[Collection[Interval]] = []
        for f in (rselect, rselect_efficiently, iselect):
            S = f(I)
            assert is_pairwise_disjoint(S), (f, S)
            solns.append(S)

        assert all(len(s) == len(solns[0]) for s in solns[1:])
        assert all(set(s) == set(solns[0]) for s in solns[1:])
        print("test passed")

    # def test2():
    #     I = Interval.random_intervals(10)
    #     print(", ".join(f"[{j.start}, {j.finish}]" for j in I))

    test()
