#!/usr/bin/env python3

from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import Any

type Edge = tuple[int, int]


def out_neighbor_lists[Vertex: Hashable](
    V: Iterable[Vertex], E: Iterable[tuple[Vertex, Vertex]]
) -> dict[Vertex, list[Vertex]]:
    out_neighbors: dict[Vertex, list[Vertex]] = {v: [] for v in V}
    for u, w in E:
        out_neighbors[u].append(w)
    return out_neighbors


def in_neighbor_lists[Vertex: Hashable](
    V: Iterable[Vertex], E: Iterable[tuple[Vertex, Vertex]]
) -> dict[Vertex, list[Vertex]]:
    return out_neighbor_lists(V, [(w, u) for u, w in E])


def random_digraph(
    n: int = 10, m: int | None = None, acyclic: bool = False
) -> tuple[list[int], list[Edge]]:
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

    def random_edge_set(n_edges: int) -> set[Edge]:
        if acyclic:
            priority = random.sample(range(n), n)

        edges: set[Edge] = set()
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


def random_graph(n: int = 10, m: int | None = None) -> tuple[list[int], list[Edge]]:
    V, E = random_digraph(n, m, acyclic=True)
    E += [(w, u) for u, w in E]
    return V, E


def random_weighted_digraph(
    *args: Any, **kwargs: Any
) -> tuple[list[int], list[Edge], dict[Edge, int]]:
    import random

    V, E = random_digraph(*args, **kwargs)
    weights = {e: random.choice(range(10000)) for e in E}
    return V, E, weights


def random_weighted_graph(
    *args: Any, **kwargs: Any
) -> tuple[list[int], list[Edge], dict[Edge, int]]:
    V, E, weights = random_weighted_digraph(*args, **kwargs, acyclic=True)
    E += [(w, u) for u, w in E]
    for u, w in E:
        weights[(w, u)] = weights[(u, w)]
    return V, E, weights


def depth_first_search[Vertex: Hashable](
    V: Iterable[Vertex],
    E: Iterable[tuple[Vertex, Vertex]],
    previsit: Callable[[Vertex, Vertex | None], object] | None = None,
    postvisit: Callable[[Vertex, Vertex | None], object] | None = None,
    source: Vertex | None = None,
) -> None:
    neighbors = out_neighbor_lists(V, E)
    visited: set[Vertex] = set()

    def DFS1(u: Vertex, parent: Vertex | None = None) -> None:
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


def breadth_first_search_parents[Vertex: Hashable](
    V: Iterable[Vertex], E: Iterable[tuple[Vertex, Vertex]], source: Vertex | None = None
) -> Iterator[tuple[Vertex, Vertex]]:
    from collections import deque

    if source is None:
        source = next(v for v in V)

    neighbors = out_neighbor_lists(V, E)

    queue: deque[Vertex] = deque()
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


def topological_sort[Vertex: Hashable](
    V: Iterable[Vertex], E: Iterable[tuple[Vertex, Vertex]]
) -> list[Vertex]:
    finished: list[Vertex] = []

    def postvisit(u: Vertex, parent: Vertex | None) -> None:
        finished.append(u)

    depth_first_search(V, E, postvisit=postvisit)

    return list(reversed(finished))
