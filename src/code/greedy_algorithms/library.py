#!/usr/bin/env python3

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

type Edge[Vertex] = tuple[Vertex, Vertex]


def out_neighbor_lists[Vertex](
    V: Iterable[Vertex], E: Iterable[Edge[Vertex]]
) -> dict[Vertex, list[Vertex]]:
    out_neighbors: dict[Vertex, list[Vertex]] = {v: [] for v in V}
    for u, w in E:
        out_neighbors[u].append(w)
    return out_neighbors


def in_neighbor_lists[Vertex](
    V: Iterable[Vertex], E: Iterable[Edge[Vertex]]
) -> dict[Vertex, list[Vertex]]:
    return out_neighbor_lists(V, [(w, u) for u, w in E])


class Heap[T: SupportsRichComparison]:
    """Heap for Dijkstra's and Prim's algorithms"""

    import heapq

    def __init__(self) -> None:
        self.array: list[T] = []

    def insert(self, item: T) -> None:
        self.heapq.heappush(self.array, item)

    def pop_min(self) -> T:
        return self.heapq.heappop(self.array)

    def empty(self) -> bool:
        return not self.array


class DisjointSet:
    """
    Disjoint-Set data structure for Kruskal's algorithm.
    (See https://en.wikipedia.org/wiki/Disjoint-set_data_structure.)
    """

    def __init__(self) -> None:
        self.parent: DisjointSet = self
        self.rank = 0

    def find(self) -> "DisjointSet":
        if self.parent == self:
            return self
        root = self.parent.find()
        self.parent = root
        return root

    def union(self, other: "DisjointSet") -> None:
        r1, r2 = self.find(), other.find()
        if r1 == r2:
            return
        # union by rank: hang the root of smaller rank under the other
        if r1.rank < r2.rank:
            r1.parent = r2
        elif r1.rank > r2.rank:
            r2.parent = r1
        else:
            r2.parent = r1
            r1.rank += 1


def random_digraph(
    n: int = 10, m: int | None = None, acyclic: bool = False
) -> tuple[list[int], list[Edge[int]]]:
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

    def random_edge_set(n_edges: int) -> set[Edge[int]]:
        if acyclic:
            priority = random.sample(range(n), n)

        edges: set[Edge[int]] = set()
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


def random_weighted_digraph(
    *args: Any, **kwargs: Any
) -> tuple[list[int], list[Edge[int]], dict[Edge[int], int]]:
    import random

    V, E = random_digraph(*args, **kwargs)
    weights = {e: random.choice(range(10000)) for e in E}
    return V, E, weights


def random_graph(*args: Any, **kwargs: Any) -> tuple[list[int], list[Edge[int]]]:
    # kwargs has no acyclic
    V, E = random_digraph(*args, **kwargs, acyclic=True)  # type: ignore[misc]
    E += [(w, u) for u, w in E]
    return V, E


def random_weighted_graph(
    *args: Any, **kwargs: Any
) -> tuple[list[int], list[Edge[int]], dict[Edge[int], int]]:
    V, E, weights = random_weighted_digraph(*args, **kwargs, acyclic=True)
    E += [(w, u) for u, w in E]
    for u, w in E:
        weights[(w, u)] = weights[(u, w)]
    return V, E, weights
