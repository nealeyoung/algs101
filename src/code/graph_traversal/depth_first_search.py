#!/usr/bin/env python3

from collections.abc import Callable, Hashable, Iterable

from graph_library import out_neighbor_lists, random_digraph, random_graph

type Visit[T] = Callable[[T, T | None], object]


def depth_first_search[T: Hashable](
    V: Iterable[T],
    E: Iterable[tuple[T, T]],
    previsit: Visit[T] | None = None,
    postvisit: Visit[T] | None = None,
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

    for v in V:
        if v not in visited:
            DFS1(v)


def topological_sort[T: Hashable](V: Iterable[T], E: Iterable[tuple[T, T]]) -> list[T] | None:
    """Return the vertices in topological order, or None if the graph has a cycle."""
    E = list(E)
    finished: list[T] = []

    def postvisit(u: T, parent: T | None) -> None:
        finished.append(u)

    depth_first_search(V, E, postvisit=postvisit)

    # G has a cycle iff the DFS has a back edge, i.e., an edge (u, w) with w finishing no earlier
    # than u (for tree, forward and cross edges, w finishes before u; a self-loop is a back edge)
    finish_time = {u: t for t, u in enumerate(finished)}
    if any(finish_time[w] >= finish_time[u] for u, w in E):
        return None

    return list(reversed(finished))


def test_topological_sort(n: int = 10, m: int | None = None) -> None:
    from random import shuffle

    V, E = random_digraph(n, m, acyclic=True)

    shuffle(V)
    order = topological_sort(V, E)
    assert order is not None

    rank = dict((v, i) for i, v in enumerate(order))

    assert all(rank[u] < rank[w] for u, w in E)

    # adding an edge that closes a cycle (or a self-loop) must be detected
    if E:
        u, w = E[0]
        assert topological_sort(V, E + [(w, u)]) is None
    assert topological_sort(V, E + [(V[0], V[0])]) is None


def count_forward_edges[T: Hashable](V: Iterable[T], E: Iterable[tuple[T, T]]) -> int:
    neighbors = out_neighbor_lists(V, E)
    visited: set[T] = set()
    being_visited: set[T] = set()
    n_forward_edges = 0

    def DFS1(u: T) -> None:
        nonlocal n_forward_edges

        visited.add(u)
        being_visited.add(u)

        for w in neighbors[u]:
            if w not in visited:
                DFS1(w)
            elif w not in being_visited:
                n_forward_edges += 1

        being_visited.remove(u)

    for v in V:
        if v not in visited:
            DFS1(v)

    return n_forward_edges


def count_connected_components[T: Hashable](V: Iterable[T], E: Iterable[tuple[T, T]]) -> int:
    # (V, E) is undirected graph

    n_components = 0

    def previsit(u: T, parent: T | None) -> None:
        nonlocal n_components
        if parent is None:
            n_components += 1

    depth_first_search(V, E, previsit=previsit)

    return n_components


def test_count_forward_edges(n: int = 10, m: int | None = None) -> None:
    V, E = random_graph(n, m)
    assert n == len(V)

    n_components = count_connected_components(V, E)
    n_tree_edges = n - n_components
    n_forward_edges = count_forward_edges(V, E)

    assert n_tree_edges + n_forward_edges == len(E) / 2


# def strong_components(G):
#     assert isinstance(G, DiGraph)

#     finished = []
#     depth_first_search(G, postvisit=lambda u, _: finished.append(u))

#     G_reversed = DiGraph(vertices=list(reversed(finished)),
#                          edges=set((w, u) for (u, w) in G.edges))

#     components = []

#     def previsit(u, tree_edge):
#         if tree_edge is None:
#             components.append([])
#         components[-1].append(u)

#     depth_first_search(G_reversed, previsit)

#     return components


# class DFS_edge_classifier:
#     def __init__(self, G):
#         self.G = G
#         self.start_times = {}
#         self.finish_times = {}

#         counter = 0

#         def time():
#             nonlocal counter
#             counter += 1
#             return counter

#         self.tree_edges = set()

#         def previsit(u, tree_edge):
#             if tree_edge is not None:
#                 self.tree_edges.add(tree_edge)
#             self.start_times[u] = time()

#         def postvisit(u, _):
#             self.finish_times[u] = time()

#         depth_first_search(G, previsit, postvisit)

#         self.forward_edges = set()
#         self.back_edges = set()
#         self.cross_edges = set()

#         for e in G.edges:
#             if e not in self.tree_edges:
#                 u, w = e
#                 s_u, f_u = self.start_times[u], self.finish_times[u]
#                 s_w, f_w = self.start_times[w], self.finish_times[w]
#                 if e == {u, w}:     # undirected edge
#                     assert s_w < s_u < f_u < f_w or s_u < s_w < f_w < f_u
#                     self.forward_edges.add(e)
#                 elif s_u < s_w < f_w < f_u:
#                     self.forward_edges.add(e)
#                 elif s_w < s_u < f_u < f_w:
#                     self.back_edges.add(e)
#                 elif s_w < f_w < s_u < f_u:
#                     self.cross_edges.add(e)
#                 else:
#                     assert False


if __name__ == "__main__":
    for _ in range(5):
        test_topological_sort(10)

    for _ in range(5):
        test_count_forward_edges(10)

    print("test passed")
