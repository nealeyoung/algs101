#!/usr/bin/env python3

from collections.abc import Collection, Iterable, Mapping
from math import inf

from library import DisjointSet, Edge, Heap, out_neighbor_lists


def Prim[Vertex](
    V: Collection[Vertex], E: Iterable[Edge[Vertex]], weights: Mapping[Edge[Vertex], float]
) -> list[Edge[Vertex]] | None:
    F: list[Edge[Vertex]] = []
    F_vertices: set[Vertex] = set()
    heap: Heap[tuple[float, Vertex, Vertex]] = Heap()  # heap of edges out of F

    neighbors = out_neighbor_lists(V, E)

    def add_to_F(u: Vertex) -> None:
        F_vertices.add(u)
        for w in neighbors[u]:
            if w not in F_vertices:
                key = weights[(u, w)]
                heap.insert((key, u, w))

    source = next(v for v in V)
    add_to_F(source)

    while not heap.empty():
        key, u, w = heap.pop_min()
        if w not in F_vertices:
            F.append((u, w))
            add_to_F(w)

    return F if len(F) == len(V) - 1 else None


def Kruskal[Vertex](
    V: Collection[Vertex], E: Iterable[Edge[Vertex]], weights: Mapping[Edge[Vertex], float]
) -> list[Edge[Vertex]] | None:
    F: list[Edge[Vertex]] = []
    subtrees = {v: DisjointSet() for v in V}

    for e in sorted(E, key=lambda e: weights[e]):
        u, w = e
        t_u, t_w = subtrees[u].find(), subtrees[w].find()
        if t_u != t_w:
            F.append(e)
            t_u.union(t_w)

    return F if len(F) == len(V) - 1 else None


if __name__ == "__main__":
    from library import random_weighted_graph

    def test(n: int = 10, m: int | None = None) -> None:
        V, E, weights = random_weighted_graph(n, m)
        F1 = Prim(V, E, weights)
        F2 = Kruskal(V, E, weights)

        def weight(F: list[Edge[int]] | None) -> float:
            return inf if F is None else sum(weights[e] for e in F)

        assert weight(F1) == weight(F2)

    for _ in range(50):
        test(100)

    print("test passed")
