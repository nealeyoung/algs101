#!/usr/bin/env python3

from collections.abc import Hashable, Iterable


def out_neighbor_lists[T: Hashable](V: Iterable[T], E: Iterable[tuple[T, T]]) -> dict[T, list[T]]:
    out_neighbors: dict[T, list[T]] = {v: [] for v in V}
    for u, w in E:
        out_neighbors[u].append(w)
    return out_neighbors


def in_neighbor_lists[T: Hashable](V: Iterable[T], E: Iterable[tuple[T, T]]) -> dict[T, list[T]]:
    return out_neighbor_lists(V, [(w, u) for u, w in E])


def random_digraph(
    n: int = 10, m: int | None = None, acyclic: bool = False
) -> tuple[list[int], list[tuple[int, int]]]:
    """
    return (vertex list, edge set) for random graph
    with n vertices and m edges
    """

    import random

    vertices = list(range(n))

    n_pairs = n * (n - 1)

    if m is None:
        m = int(n_pairs / 2)
    else:
        assert 0 <= m <= n_pairs

    def random_edge_set(n_edges: int) -> set[tuple[int, int]]:
        if acyclic:
            priority = random.sample(range(n), n)

        edges: set[tuple[int, int]] = set()
        while len(edges) < n_edges:
            u, w = random.choice(vertices), random.choice(vertices)
            if u != w:
                if acyclic and priority[u] < priority[w]:
                    u, w = w, u
                edges.add((u, w))
        return edges

    if m <= n_pairs / 2:
        edges = random_edge_set(m)
    else:
        # if most edges are present, faster to generate the complement
        all_pairs = set((u, w) for u in vertices for w in vertices if u != w)
        assert len(all_pairs) == n_pairs
        edges = all_pairs - random_edge_set(n_pairs - m)

    assert len(vertices) == n
    assert len(edges) == m
    return vertices, list(edges)


def random_graph(n: int = 10, m: int | None = None) -> tuple[list[int], list[tuple[int, int]]]:
    V, E = random_digraph(n, m, acyclic=True)
    E += [(w, u) for u, w in E]
    return V, E
