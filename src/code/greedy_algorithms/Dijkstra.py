#!/usr/bin/env python3

from collections.abc import Iterable, Mapping
from math import inf

from library import Edge, Heap, in_neighbor_lists, out_neighbor_lists


def Dijkstra[Vertex](
    V: Iterable[Vertex],
    E: Iterable[Edge[Vertex]],
    weights: Mapping[Edge[Vertex], float],
    source: Vertex,
) -> dict[Vertex, float]:
    assert all(w >= 0 for w in weights.values())

    neighbors = out_neighbor_lists(V, E)

    heap: Heap[tuple[float, tuple[Vertex | None, Vertex]]] = Heap()  # heap of edges out of K
    d: dict[Vertex, float] = {}

    heap.insert((0, (None, source)))  # first iteration: w = source

    while not heap.empty():
        key, (_, w) = heap.pop_min()
        if w not in d:
            d[w] = key
            for x in neighbors[w]:
                if x not in d:
                    key = d[w] + weights[(w, x)]
                    heap.insert((key, (w, x)))

    for v in V:
        if v not in d:
            d[v] = inf

    return d


def check_shortest_path_distances[Vertex](
    V: Iterable[Vertex],
    E: Iterable[Edge[Vertex]],
    weights: Mapping[Edge[Vertex], float],
    source: Vertex,
    d: Mapping[Vertex, float],
) -> bool:
    in_neighbors = in_neighbor_lists(V, E)

    return d[source] == 0 and all(
        d[w] == min((d[u] + weights[(u, w)] for u in in_neighbors[w]), default=inf)
        for w in V
        if w != source
    )


if __name__ == "__main__":
    from library import random_weighted_digraph

    def test(n: int = 10, m: int | None = None) -> None:
        V, E, weights = random_weighted_digraph(n, m)
        source = next(v for v in V)
        d = Dijkstra(V, E, weights, source)
        assert check_shortest_path_distances(V, E, weights, source, d)

    for _ in range(50):
        test(100)

    print("test passed")
