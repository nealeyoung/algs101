#!/usr/bin/env python3

from collections.abc import Collection, Iterator, Sequence

# preferences[i] lists, in order of preference, the people that person i ranks
type Preferences = Sequence[Sequence[int]]
type Matching = Collection[tuple[int, int]]


class Person:
    def __init__(self, preferences: Sequence[int]) -> None:
        self.preferences = preferences
        self.ranks = [0] * len(preferences)  # allocate array
        for r, p in enumerate(preferences):
            self.ranks[p] = r
        self.partner: int | None = None
        self.partner_iterator = iter(self.preferences)

    def prefers(self, p1: int, p2: int) -> bool:
        return self.ranks[p1] < self.ranks[p2]


def Gale_Shapley(
    hospitals_preferences: Preferences, doctors_preferences: Preferences
) -> set[tuple[int, int]]:
    """The Gale-Shapley algorithm for stable matching"""

    hospitals = tuple(Person(p) for p in hospitals_preferences)
    doctors = tuple(Person(p) for p in doctors_preferences)

    unmatched_hospitals = list(range(len(hospitals)))

    while unmatched_hospitals:
        h = unmatched_hospitals.pop()
        D = doctors[next(hospitals[h].partner_iterator)]

        if D.partner is None:
            D.partner = h
        elif D.prefers(D.partner, h):
            unmatched_hospitals.append(h)
        else:
            unmatched_hospitals.append(D.partner)
            D.partner = h

    return set((D.partner, d) for d, D in enumerate(doctors))  # type: ignore[misc] # all matched


def unstable_pairs(
    hospitals_preferences: Preferences, doctors_preferences: Preferences, M: Matching
) -> Iterator[tuple[int, int]]:
    hospitals = [Person(p) for p in hospitals_preferences]
    doctors = [Person(p) for p in doctors_preferences]

    for h, d in M:
        hospitals[h].partner = d
        doctors[d].partner = h

    for h, H in enumerate(hospitals):
        for d, D in enumerate(doctors):
            # M is perfect, so H.partner and D.partner aren't None
            if H.prefers(d, H.partner) and D.prefers(h, D.partner):  # type: ignore[arg-type]
                yield (h, d)


def is_stable(
    hospitals_preferences: Preferences, doctors_preferences: Preferences, M: Matching
) -> bool:
    return not any(unstable_pairs(hospitals_preferences, doctors_preferences, M))


def exhaustive_search(
    hospitals_preferences: Preferences, doctors_preferences: Preferences
) -> set[tuple[int, int]] | None:
    """Exhaustive search to find a stable matching"""

    from itertools import permutations

    n = len(hospitals_preferences)

    for p in permutations(range(n)):
        M = {(i, p[i]) for i in range(n)}
        if is_stable(hospitals_preferences, doctors_preferences, M):
            return M

    return None


def old_algorithm(
    hospitals_preferences: Preferences, doctors_preferences: Preferences
) -> list[tuple[int, int]]:
    """Old algorithm from LN 3 Fig. 2"""

    n = len(hospitals_preferences)
    assert n == 3

    hospitals = [Person(p) for p in hospitals_preferences]
    doctors = [Person(p) for p in doctors_preferences]

    pairs_by_rank: list[list[list[tuple[int, int]]]] = [[[] for _ in range(n)] for _ in range(n)]

    for h, H in enumerate(hospitals):
        for d, D in enumerate(doctors):
            i, j = H.ranks[d], D.ranks[h]
            pairs_by_rank[i][j].append((h, d))

    M: list[tuple[int, int]] = []

    for i, j in ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 2), (2, 3), (3, 2), (3, 3)):
        for h, d in pairs_by_rank[i - 1][j - 1]:
            H, D = hospitals[h], doctors[d]
            if H.partner is None and D.partner is None:
                M.append((h, d))
                H.partner = d
                D.partner = h

    assert len(M) == 3
    return M


def test_Gale_Shapley(n: int = 10) -> None:
    from random import sample

    prefs = [[sample(tuple(range(n)), n) for _ in range(n)] for _ in range(2)]

    M = Gale_Shapley(*prefs)
    assert is_stable(*prefs, M)  # type: ignore[call-arg, arg-type] # prefs has 2 items


def test_exhaustive_search(n: int = 5) -> None:
    from random import sample

    prefs = [[sample(tuple(range(n)), n) for _ in range(n)] for _ in range(2)]

    M = exhaustive_search(*prefs)
    assert is_stable(*prefs, M)  # type: ignore[call-arg, arg-type] # prefs has 2 items


def test_old_algorithm() -> bool:
    from random import sample

    n = 3

    prefs = [[sample(tuple(range(n)), n) for _ in range(n)] for _ in range(2)]

    M = old_algorithm(*prefs)
    if not is_stable(*prefs, M):  # type: ignore[call-arg, arg-type] # prefs has 2 items
        return False
    return True


if __name__ == "__main__":
    print(
        "old_algorithm produced",
        len([stable for stable in [test_old_algorithm() for _ in range(100)] if stable]),
        "stable matchings out of 100",
    )

    for n in range(5, 20):
        test_Gale_Shapley(n)
        print(f"Gale_Shapley({n}) passed")

    for n in range(5, 9):  # exhaustive search takes time n!, so keep n small
        test_exhaustive_search(n)
        print(f"exhaustive_search({n}) passed")
