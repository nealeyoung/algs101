#!/usr/bin/env python3

type Tree = InteriorNode | Leaf


class InteriorNode:
    def __init__(self, left: Tree, right: Tree) -> None:
        self.left = left
        self.right = right
        self.frequency: int = left.frequency + right.frequency
        self.cost: int = self.frequency + left.cost + right.cost

    def split(self, p1: int, p2: int) -> Tree:
        split_left = self.left.split(p1, p2)
        if split_left != self.left:
            return InteriorNode(split_left, self.right)

        split_right = self.right.split(p1, p2)
        if split_right != self.right:
            return InteriorNode(self.left, split_right)

        return self


class Leaf:
    def __init__(self, frequency: int) -> None:
        self.frequency = frequency
        self.cost = 0

    def split(self, p1: int, p2: int) -> Tree:
        if self.frequency == p1 + p2:
            return InteriorNode(Leaf(p1), Leaf(p2))
        else:
            return self


def Huffman(p: list[int]) -> Tree:
    if len(p) == 1:
        return Leaf(p[0])

    p1, p2 = p[:2]

    p_prime = sorted([p1 + p2] + p[2:])
    R = Huffman(p_prime)
    T = R.split(p1, p2)
    return T


def iHuffman(p: list[int]) -> Tree:
    from collections import deque

    assert all(p1 <= p2 for p1, p2 in zip(p, p[1:]))

    C1 = deque(Leaf(p_i) for p_i in p)
    C2: deque[InteriorNode] = deque()

    def get_next_tree() -> Tree:
        if not C2 or (C1 and C1[0].frequency < C2[0].frequency):
            return C1.popleft()
        return C2.popleft()

    for _ in range(len(p) - 1):
        t1, t2 = get_next_tree(), get_next_tree()
        t = InteriorNode(t1, t2)
        C2.append(t)

    return C2[0] if C2 else C1[0]  # just a leaf if len(p) == 1


if __name__ == "__main__":

    def random_p(n: int, m: int | None = None) -> list[int]:
        import random

        if n <= 0:
            return []

        if not m:
            m = 2 * n

        return sorted(random.randrange(m) for _ in range(n))

    def test() -> None:
        p = random_p(n=100)

        solns: list[Tree] = []
        for f in (Huffman, iHuffman):
            t = f(p)
            solns.append(t)

        assert all(t.cost == solns[0].cost for t in solns[1:])
        print("test passed")

    test()
