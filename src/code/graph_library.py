#!/usr/bin/env python3

from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import Any


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


def random_weighted_digraph(
    *args: Any, **kwargs: Any
) -> tuple[list[int], list[tuple[int, int]], dict[tuple[int, int], int]]:
    import random

    V, E = random_digraph(*args, **kwargs)
    weights = {e: random.choice(range(10000)) for e in E}
    return V, E, weights


def random_weighted_graph(
    *args: Any, **kwargs: Any
) -> tuple[list[int], list[tuple[int, int]], dict[tuple[int, int], int]]:
    V, E, weights = random_weighted_digraph(*args, **kwargs, acyclic=True)
    E += [(w, u) for u, w in E]
    for u, w in E:
        weights[(w, u)] = weights[(u, w)]
    return V, E, weights


type Visit[T] = Callable[[T, T | None], object]


def depth_first_search[T: Hashable](
    V: Iterable[T],
    E: Iterable[tuple[T, T]],
    previsit: Visit[T] | None = None,
    postvisit: Visit[T] | None = None,
    source: T | None = None,
) -> None:
    neighbors = out_neighbor_lists(V, E)
    visited: set[T] = set()

    def DFS1(u: T, parent: T | None = None) -> None:
        visited.add(u)
        if previsit:
            previsit(u, parent)
        for w in neighbors[u]:
            if w not in visited:
                DFS1(w, u)
        if postvisit:
            postvisit(u, parent)

    if source is not None:
        DFS1(source)
    else:
        for v in V:
            if v not in visited:
                DFS1(v)


def breadth_first_search_parents[T: Hashable](
    V: Iterable[T], E: Iterable[tuple[T, T]], source: T | None = None
) -> Iterator[tuple[T, T]]:
    from collections import deque

    if source is None:
        source = next(v for v in V)

    neighbors = out_neighbor_lists(V, E)

    queue: deque[T] = deque()
    queue.append(source)
    visited = {source}

    while queue:
        u = queue.popleft()
        for w in neighbors[u]:
            if w not in visited:
                visited.add(w)
                queue.append(w)
                yield (w, u)

    # for v in V:
    #     if v not in d:
    #         d[v] = inf

    # return d, parents


def topological_sort[T: Hashable](V: Iterable[T], E: Iterable[tuple[T, T]]) -> list[T]:
    finished: list[T] = []

    def postvisit(u: T, parent: T | None) -> None:
        finished.append(u)

    depth_first_search(V, E, postvisit=postvisit)

    return list(reversed(finished))
