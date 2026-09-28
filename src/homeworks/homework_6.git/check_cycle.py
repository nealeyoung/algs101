#!/usr/bin/env python3
"""Check an answer to Homework 6, Problem 5(a): a cycle, starting at node a,
that traverses each edge of the problem's graph once in each direction.

Usage:  python3 check_cycle.py "(a, b), (b, f), ..."
   or:  python3 check_cycle.py        (then paste the cycle and press Ctrl-D)
"""

import re
import sys

# the graph drawn in Problem 5 (undirected)
EDGES = [
    ("a", "b"),
    ("a", "c"),
    ("a", "d"),
    ("b", "f"),
    ("c", "e"),
    ("c", "d"),
    ("d", "e"),
    ("e", "h"),
    ("g", "h"),
]
START = "a"


def check(cycle: list[tuple[str, str]]) -> list[str]:
    """Return a list of problems with the cycle (empty if it is correct)."""
    problems = []
    if not cycle:
        return ["the cycle is empty"]
    if cycle[0][0] != START:
        problems.append(f"the cycle should start at node {START}")
    for (u1, w1), (u2, w2) in zip(cycle, cycle[1:] + cycle[:1]):
        if w1 != u2:
            problems.append(f"edge ({u2}, {w2}) doesn't start where ({u1}, {w1}) ends")
    wanted = {(u, w) for u, w in EDGES} | {(w, u) for u, w in EDGES}
    for e in sorted(wanted - set(cycle)):
        problems.append(f"edge ({e[0]}, {e[1]}) is missing")
    for e in sorted(set(cycle) - wanted):
        problems.append(f"({e[0]}, {e[1]}) is not an edge of the graph")
    for e in sorted(set(cycle)):
        if cycle.count(e) > 1:
            problems.append(f"edge ({e[0]}, {e[1]}) occurs {cycle.count(e)} times")
    return problems


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    cycle = re.findall(r"\(\s*([a-z])\s*,\s*([a-z])\s*\)", text)
    problems = check(cycle)
    if problems:
        print("Not a correct cycle:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"Correct: a cycle of {len(cycle)} directed edges, starting at {START}.")
