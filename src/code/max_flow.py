#!/usr/bin/env python3

from collections.abc import Hashable, Mapping, Set
from typing import Any

from graph_library import (
    breadth_first_search_parents,
    depth_first_search,
    in_neighbor_lists,
    out_neighbor_lists,
)


def Ford_Fulkerson[T: Hashable](
    V: Set[T],
    E: Set[tuple[T, T]],
    caps: Mapping[tuple[T, T], int],
    s: T,
    t: T,
    use_BFS: bool = False,
) -> dict[tuple[T, T], int]:
    assert all((w, u) not in E for (u, w) in E)

    f = {(u, w): 0 for (u, w) in E}

    def cap(u: T, w: T) -> int:
        return caps[u, w]

    def residual_cap(u: T, w: T) -> int:
        return cap(u, w) - f[u, w] if (u, w) in E else f[w, u]

    while True:
        Ef = set((u, w) for (u, w) in E if f[u, w] < cap(u, w)) | set(
            (w, u) for (u, w) in E if f[u, w] > 0
        )

        if not use_BFS:
            parents: dict[T, T | None] = {}

            def previsit(w: T, u: T | None) -> None:
                if u is not None:
                    parents[w] = u  # noqa: B023 (previsit is used only in this iteration)

            depth_first_search(V, Ef, previsit=previsit, source=s)
        else:
            parents = dict(breadth_first_search_parents(V, Ef, s))

        if t not in parents:
            break

        path: list[Any] = [t]  # a list of vertices, then (below) of edges
        while path[-1] in parents:
            path.append(parents[path[-1]])
        assert path[-1] == s

        path = list(reversed(path))
        path = list(zip(path, path[1:]))  # list of vertices -> list of edges

        delta = min(residual_cap(u, w) for (u, w) in path)
        for u, w in path:
            if (u, w) in E:
                f[u, w] += delta
            else:
                f[w, u] -= delta

        assert delta > 0

    # done. verify then return f

    # verify flow value is cut capacity

    in_neighbors = in_neighbor_lists(V, E)
    out_neighbors = out_neighbor_lists(V, E)

    parents[s] = None

    value = sum(f[s, w] for w in out_neighbors[s])
    cut_capacity = sum(cap(u, w) for (u, w) in E if u in parents and w not in parents)
    assert value == cut_capacity

    # verify capacity constraints

    assert all(0 <= f[u, w] <= cap(u, w) for u, w in E)

    # verify conservation constraints

    assert all(
        sum(f[u, v] for u in in_neighbors[v]) == sum(f[v, w] for w in out_neighbors[v])
        for v in V - {s, t}
    )
    return f


def Edmonds_Karp[T: Hashable](
    V: Set[T], E: Set[tuple[T, T]], capacities: Mapping[tuple[T, T], int], s: T, t: T
) -> dict[tuple[T, T], int]:
    return Ford_Fulkerson(V, E, capacities, s, t, use_BFS=True)


def test_max_flow() -> None:
    s, a, b, t = "sabt"
    V = {s, a, b, t}
    capacities = {(s, a): 9, (s, b): 5, (a, b): 5, (a, t): 6, (b, t): 7}
    E = capacities.keys()

    f1 = Ford_Fulkerson(V, E, capacities, s, t)
    f2 = Edmonds_Karp(V, E, capacities, s, t)
    value1 = sum(f1[s, w] for (u, w) in E if u == s)
    value2 = sum(f2[s, w] for (u, w) in E if u == s)

    assert value1 == value2 == 13


if __name__ == "__main__":
    test_max_flow()

    print("test passed")
