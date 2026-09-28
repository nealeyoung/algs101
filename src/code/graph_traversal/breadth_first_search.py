#!/usr/bin/env python3

from collections import deque
from collections.abc import Hashable, Iterable, Mapping
from math import inf

from graph_library import in_neighbor_lists, out_neighbor_lists, random_digraph


def minf(collection: Iterable[float]) -> float:
    return min(collection, default=inf)


def breadth_first_search[T: Hashable](
    V: Iterable[T], E: Iterable[tuple[T, T]], source: T | None = None
) -> dict[T, float]:
    if source is None:
        source = next(v for v in V)

    neighbors = out_neighbor_lists(V, E)

    queue: deque[T] = deque()
    d: dict[T, float] = {source: 0}
    queue.append(source)

    while queue:
        u = queue.popleft()
        for w in neighbors[u]:
            if w not in d:
                d[w] = d[u] + 1
                queue.append(w)

    for v in V:
        if v not in d:
            d[v] = inf

    return d


def check_unweighted_shortest_path_distances[T: Hashable](
    V: Iterable[T], E: Iterable[tuple[T, T]], source: T, d: Mapping[T, float]
) -> bool:
    in_neighbors = in_neighbor_lists(V, E)

    return d[source] == 0 and all(
        d[w] == minf(d[u] + 1 for u in in_neighbors[w]) for w in V if w != source
    )


if __name__ == "__main__":

    def test_BFS(n: int = 10, m: int | None = None) -> None:
        V, E = random_digraph(n, m)
        source = next(v for v in V)
        d = breadth_first_search(V, E, source)
        assert check_unweighted_shortest_path_distances(V, E, source, d)

    for _ in range(50):
        test_BFS(100)

    print("test passed")
